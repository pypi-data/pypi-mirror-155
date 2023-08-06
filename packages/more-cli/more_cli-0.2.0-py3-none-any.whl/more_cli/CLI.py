from pyfiglet import Figlet
import inquirer
import os
import zipfile
import requests
import json
import re


def extractRequirements(file):
    test = open(file, 'r')
    result = []
    for pkg in test.readlines():
        package = re.findall(r'^import [a-zA-Z0-9]+|^from [a-zA-Z0-9]+', pkg)
        if len(package) > 0:
            tmp = package[0].replace('import ', '')
            tmp = tmp.replace('from ', '')
            if not tmp in result:
                result.append(tmp)
    return result


def zip_directory(folder_path, zip_path):
    reqs = []
    with zipfile.ZipFile(zip_path, mode='w') as zipf:
        len_dir_path = len(folder_path)
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if '.py' in file and '.pyc' not in file and 'MORE-CLI' not in file_path:
                    reqs += extractRequirements(file_path)
                if file not in config['ignore']['files'] and 'MORE-CLI' not in file_path:
                    zipf.write(file_path, file_path[len_dir_path:])
    return list(set(reqs))


title = Figlet(font='slant')
print('\u001b[34m')
print(title.renderText('M O R E - CLI'))
print('\u001b[0m')

# load Configuration if exist
if os.path.exists('cli_config.json'):
    with open('cli_config.json', 'r') as f:
        config = json.load(f)
else:
    config = {}
    print('Set IP-Adress and Host of CoordinationServer: (example: 127.0.0.1:3000)')
    config['url'] = input()
    config['ignore'] = {"files":["code.zip", "CLI.py", "cli_config.json"],"folder":["MORE-CLI"]}

zip_directory(os.getcwd(),'code.zip')
if config.get('experiment') is None:
    if config.get('project') is None:
        projects = requests.request('GET', 'http://' + config['url'] + '/project/getAll', headers={}, files=[]).json()[
            'result']
        active = list(filter(lambda p: 'Active' in p['status'], projects))
        questions = [
            inquirer.List(
                "name",
                message="Choose your Project?",
                choices=[p['name'] for p in active],
            ),
        ]

        answers = inquirer.prompt(questions)
        for x in projects:
            if x['name'] == answers['name']:
                config['project'] = x
                break

    if config.get('type') is None:
        questions = [
            inquirer.List(
                "type",
                message="Choose an Experiment-Type?",
                choices=['Trial', 'Optimization'],
            ),
        ]

        answers = inquirer.prompt(questions)
        config['type'] = answers['type']
        if answers['type'] == 'Optimization':
            questions = [
                inquirer.List(
                    "direction",
                    message="Optimization-Direction?",
                    choices=['minimize', 'maximize'],
                ),
            ]
            answers = inquirer.prompt(questions)
            opti = {'direction': answers['direction']}
            print('How many Agents should perform parallel? (Default = 1)')
            agents = input()
            opti['agents'] = agents
            print('How many Trials should be trained?')
            trials = input()
            opti['trials'] = trials
            config['optimization'] = opti

    # Parameter
    if config.get('parameter') is None and config.get('optimization') is None:
        tmp = []
        while True:
            print('Add Parameter? [y/n]')
            a = input()
            if a == 'Y' or a == 'y':
                print('Choose a Name:')
                name = input()
                print('Set Value of ' + name + ':')
                value = input()
                parameter = {"name": name, "value": value}
                tmp.append(parameter)
            else:
                config['parameter'] = tmp
                break

    if config.get('parameter') is None and config.get('optimization') is not None:
        tmp = []
        while True:
            print('Add Parameter? [y/n]')
            a = input()
            if a == 'Y' or a == 'y':
                print('Choose a Name:')
                name = input()
                parameter = {"name": name}
                questions = [
                    inquirer.List(
                        "type",
                        message="Choose a Parameter-Type!",
                        choices=['float', 'int', 'string'],
                    ),
                ]
                answers = inquirer.prompt(questions)
                parameter['type'] = answers['type']
                if not parameter['type'] == 'string':
                    print('Minimum:')
                    parameter['min'] = input()
                    print('Maximum:')
                    parameter['max'] = input()
                    print("Stepsize (0 = Empty):")
                    stepsize = input()
                    if stepsize != '0':
                        parameter['stepsize'] = stepsize
                else:
                    print('Categorical Values: (example: ["Name1","Name2","Name3"]')
                    cats = input()
                    parameter['catvalues'] = json.loads(cats)
                tmp.append(parameter)
            else:
                config['parameter'] = tmp
                break
    # Versions-nummer
    versions = \
        requests.request('GET',
                         'http://' + config['url'] + '/project/VersionCodes?project_name=' + config['project']['name'],
                         headers={}, files=[]).json()['result']

    print('Do you want to use an existing Version? [y/n]')
    aw = input()
    if aw == 'y' or aw == 'Y':
        questions = [
            inquirer.List(
                "version",
                message="Choose an existing Version:",
                choices=versions,
            ),
        ]
        answer = inquirer.prompt(questions)
        config['version'] = answer['version']
    else:
        print('Set Version: (>' + max(versions) + ')')
        config['version'] = input()

    requirements = zip_directory(os.getcwd(), os.getcwd() + '/code.zip')
    config['requirements'] = requirements

    with open('../../../MORE-CLI/cli_config.json', 'w') as r:
        json.dump(config, r)

    if config.get('optimization') is not None:
        payload = {
            'optimization': {'direction': config['optimization']['direction'], 'n_agents': config['optimization']['agents'],
                             'trials': config['optimization']['trials']},
            'requirements': config['requirements'], 'version': config['version']}
        payload['parameterranges'] = config['parameter']
        if aw == 'y' or aw == 'Y':
            files = []
        else:
            files = [('file', ('code.zip', open(os.getcwd() + '/code.zip', 'rb'), 'application/zip'))]
        headers = {}

        response = requests.request("POST",
                                    'http://' + config['url'] + '/project/createOptimization?project_id=' +
                                    config['project']['_id'],
                                    headers=headers,
                                    data={'experiment': json.dumps(payload)}, files=files)
        exp = response.json()['experiment']
    else:
        payload = {'requirements': config['requirements'], 'version': config['version']}
        payload['parametervalues'] = config['parameter']
        if aw == 'y' or aw == 'Y':
            files = []
        else:
            files = [('file', ('code.zip', open(os.getcwd() + '/code.zip', 'rb'), 'application/zip'))]
        headers = {}

        response = requests.request("POST",
                                    'http://' + config['url'] + '/project/createTrial?project_id=' + config['project'][
                                        '_id'],
                                    headers=headers,
                                    files=files, data={"experiment": json.dumps(payload)})
        exp = response.json()['experiment']

    config['experiment'] = exp
    print('Experiment has been created \u001b[32m successfully! \u001b[0m \n\r')

print('Do you want to start the Experiment? [y/n]')
choice = input()
if config.get('notification') is None:
    print('Set an email address for notifications or press Enter:')
    email = input()
    if email != '':
        config['notification'] = email
if config.get('notification') is not None:
    requests.request("PUT", 'http://' + config['url'] + '/project/putExperiment?exp_id=' + config['experiment']['_id'],
                     headers={}, data={"notification": config['notification']})
if choice == 'y' or choice == 'Y':
    workstations = requests.request('GET', 'http://' + config['url'] + '/workstation/getAllWorkstations').json()[
        'result']
    questions = [
        inquirer.List(
            "workstation",
            message="Choose a Workstation:",
            choices=[ws['name'] for ws in workstations],
        ),
    ]
    answer = inquirer.prompt(questions)
    workstation_id = answer['workstation']
    if config['type'] == 'Trial':
        print('Start to prepare the Python-Environment...')
        requests.request('POST',
                         'http://' + config[
                             'url'] + '/workstation/checkRequirements?project_id={}&workstation={}&env={}&exp_no={}'.format(
                             config['project']['_id'],
                             workstation_id, config['project']['env'], config['experiment']['no']),
                         data={})
        print('Python-Environment has been prepared \u001b[32m successfully! \u001b[0m \n\r')
        print('Execute Trial...')
        response = requests.request('POST',
                                    'http://' + config['url'] + '/workstation/executeTrial?project_id=' +
                                    config['project']['_id'] + '&exp_id=' + config['experiment']['_id'] + '&workstation=' + workstation_id)
        print('Experiment has been started \u001b[32m successfully! \u001b[0m')
        print('Press Enter to finish...')
        input()
    else:
        print('Start to prepare the Python-Environment...')
        requests.request('POST', 'http://' + config[
            'url'] + '/workstation/checkRequirements?project_id={}&workstation={}&env={}&exp_no={}'.format(
            config['project']['_id'],
            workstation_id, config['project']['env'], config['experiment']['no']),
                         data={})
        print('Python-Environment has been prepared \u001b[32m successfully! \u001b[0m \n\r')
        print('Execute Optimization...')
        response = requests.request('POST',
                                    'http://' + config['url'] + '/workstation/executeOptimization?project_id=' +
                                    config['project']['_id'] + '&exp_id=' +
                                    config['experiment']['_id'] + '&workstation=' + workstation_id)
        print('Experiment has been started \u001b[32m successfully! \u001b[0m')
        print('Press Enter to finish...')
        input()
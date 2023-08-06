import platform
from pyfiglet import Figlet
import inquirer
from pick import pick
import os
import zipfile
import requests
import json
import re


class CLIWindows:
    def extractRequirements(self,file):
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


    def zip_directory(self,folder_path, zip_path):
        reqs = []
        with zipfile.ZipFile(zip_path, mode='w') as zipf:
            len_dir_path = len(folder_path)
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if '.py' in file and '.pyc' not in files:
                        reqs += self.extractRequirements(file_path)
                    if file not in self.config['ignore']['files']:
                        zipf.write(file_path, file_path[len_dir_path:])
        return list(set(reqs))


    def __init__(self):
        title = Figlet(font='slant')
        print('\u001b[34m')
        print(title.renderText('M O R E - CLI'))
        print('\u001b[0m')

        # load Configuration if exist
        if os.path.exists('../../../MORE-CLI/cli_config.json'):
            with open('../../../MORE-CLI/cli_config.json', 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {}
            print('Set IP-Adress and Host of CoordinationServer: (example: 127.0.0.1:3000)')
            self.config['url'] = input()
            self.config['ignore'] = {"files":["code.zip", "cli_config.json"]}

        if self.config.get('experiment') is None:
            if self.config.get('project') is None:
                projects = requests.request('GET', 'http://' + self.config['url'] + '/project/getAll', headers={}, files=[]).json()[
                    'result']
                active = list(filter(lambda p: 'Active' in p['status'], projects))
                title = 'Choose your Project?'
                options = [p['name'] for p in active]

                answers, index = pick(options, title, indicator='=>', default_index=0)

                for x in projects:
                    if x['name'] == answers:
                        self.config['project'] = x
                        break

            if self.config.get('type') is None:

                title = 'Choose an Experiment-Type?'
                options = ['Trial', 'Optimization']

                answers, index = pick(options, title, indicator='=>', default_index=0)

                self.config['type'] = answers
                if answers == 'Optimization':
                    title = "Optimization-Direction?"
                    options = ['minimize', 'maximize']

                    answers, index = pick(options, title, indicator='=>', default_index=0)
                    opti = {'direction': answers}
                    print('How many Agents should perform parallel? (Default = 1)')
                    agents = input()
                    opti['agents'] = agents
                    print('How many Trials should be trained?')
                    trials = input()
                    opti['trials'] = trials
                    self.config['optimization'] = opti

            # Parameter
            if self.config.get('parameter') is None and self.config.get('optimization') is None:
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
                        self.config['parameter'] = tmp
                        break

            if self.config.get('parameter') is None and self.config.get('optimization') is not None:
                tmp = []
                while True:
                    print('Add Parameter? [y/n]')
                    a = input()
                    if a == 'Y' or a == 'y':
                        print('Choose a Name:')
                        name = input()
                        parameter = {"name": name}

                        title = "Choose a Parameter-Type!"
                        options = ['float', 'int', 'string']

                        answers, index = pick(options, title, indicator='=>', default_index=0)

                        parameter['type'] = answers
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
                        self.config['parameter'] = tmp
                        break
            # Versions-nummer
            versions = \
                requests.request('GET',
                                 'http://' + self.config['url'] + '/project/VersionCodes?project_name=' + self.config['project']['name'],
                                 headers={}, files=[]).json()['result']

            print('Do you want to use an existing Version? [y/n]')
            aw = input()
            if aw == 'y' or aw == 'Y':

                title = 'Choose an existing Version:'
                options = versions

                answer, index = pick(options, title, indicator='=>', default_index=0)

                self.config['version'] = answer
            else:
                print('Set Version: (>' + max(versions) + ')')
                self.config['version'] = input()

            requirements = self.zip_directory(os.getcwd(), os.getcwd() + '/code.zip')
            self.config['requirements'] = requirements

            with open('../../../MORE-CLI/cli_config.json', 'w') as r:
                json.dump(self.config, r)

            if self.config.get('optimization') is not None:
                payload = {
                    'optimization': {'direction': self.config['optimization']['direction'], 'n_agents': self.config['optimization']['agents'],
                                     'trials': self.config['optimization']['trials']},
                    'requirements': self.config['requirements'], 'version': self.config['version']}
                payload['parameterranges'] = self.config['parameter']
                if aw == 'y' or aw == 'Y':
                    files = []
                else:
                    files = [('file', ('code.zip', open(os.getcwd() + '/code.zip', 'rb'), 'application/zip'))]
                headers = {}

                response = requests.request("POST",
                                            'http://' + self.config['url'] + '/project/createOptimization?project_id=' +
                                            self.config['project']['_id'],
                                            headers=headers,
                                            data={'experiment': json.dumps(payload)}, files=files)
                exp = response.json()['experiment']
            else:
                payload = {'requirements': self.config['requirements'], 'version': self.config['version']}
                payload['parametervalues'] = self.config['parameter']
                if aw == 'y' or aw == 'Y':
                    files = []
                else:
                    files = [('file', ('code.zip', open(os.getcwd() + '/code.zip', 'rb'), 'application/zip'))]
                headers = {}

                response = requests.request("POST",
                                            'http://' + self.config['url'] + '/project/createTrial?project_id=' + self.config['project'][
                                                '_id'],
                                            headers=headers,
                                            files=files, data={"experiment": json.dumps(payload)})
                exp = response.json()['experiment']

            self.config['experiment'] = exp
            print('Experiment has been created \u001b[32m successfully! \u001b[0m \n\r')

        print('Do you want to start the Experiment? [y/n]')
        choice = input()
        if self.config.get('notification') is None:
            print('Set an email address for notifications or press Enter:')
            email = input()
            if email != '':
                self.config['notification'] = email
        if self.config.get('notification') is not None:
            requests.request("PUT", 'http://' + self.config['url'] + '/project/putExperiment?exp_id=' + self.config['experiment']['_id'],
                             headers={}, data={"notification": self.config['notification']})
        if choice == 'y' or choice == 'Y':
            workstations = requests.request('GET', 'http://' + self.config['url'] + '/workstation/getAllWorkstations').json()[
                'result']

            title = 'Choose a Workstation:'
            options = [ws['name'] for ws in workstations]

            answer, index = pick(options, title, indicator='=>', default_index=0)
            workstation_id = answer
            if self.config['type'] == 'Trial':
                print('Start to prepare the Python-Environment...')
                requests.request('POST',
                                 'http://' + self.config[
                                     'url'] + '/workstation/checkRequirements?project_id={}&workstation={}&env={}&exp_no={}'.format(
                                     self.config['project']['_id'],
                                     workstation_id, self.config['project']['env'], self.config['experiment']['no']),
                                 data={})
                print('Python-Environment has been prepared \u001b[32m successfully! \u001b[0m \n\r')
                print('Execute Trial...')
                response = requests.request('POST',
                                            'http://' + self.config['url'] + '/workstation/executeTrial?project_id=' +
                                            self.config['project']['_id'] + '&exp_id=' + self.config['experiment']['_id'] + '&workstation=' + workstation_id)
                print('Experiment has been started \u001b[32m successfully! \u001b[0m')
                print('Press Enter to finish...')
                input()
            else:
                print('Start to prepare the Python-Environment...')
                requests.request('POST', 'http://' + self.config[
                    'url'] + '/workstation/checkRequirements?project_id={}&workstation={}&env={}&exp_no={}'.format(
                    self.config['project']['_id'],
                    workstation_id, self.config['project']['env'], self.config['experiment']['no']),
                                 data={})
                print('Python-Environment has been prepared \u001b[32m successfully! \u001b[0m \n\r')
                print('Execute Optimization...')
                response = requests.request('POST',
                                            'http://' + self.config['url'] + '/workstation/executeOptimization?project_id=' +
                                            self.config['project']['_id'] + '&exp_id=' +
                                            self.config['experiment']['_id'] + '&workstation=' + workstation_id)
                print('Experiment has been started \u001b[32m successfully! \u001b[0m')
                print('Press Enter to finish...')
                input()


class CLI:
    def extractRequirements(self, file):
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


    def zip_directory(self, folder_path, zip_path):
        reqs = []
        with zipfile.ZipFile(zip_path, mode='w') as zipf:
            len_dir_path = len(folder_path)
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if '.py' in file and '.pyc' not in file and 'MORE-CLI' not in file_path:
                        reqs += self.extractRequirements(file_path)
                    if file not in self.config['ignore']['files'] and 'MORE-CLI' not in file_path:
                        zipf.write(file_path, file_path[len_dir_path:])
        return list(set(reqs))

    def __init__(self):
        title = Figlet(font='slant')
        print('\u001b[34m')
        print(title.renderText('M O R E - CLI'))
        print('\u001b[0m')

        # load Configuration if exist
        if os.path.exists('cli_config.json'):
            with open('cli_config.json', 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {}
            print('Set IP-Adress and Host of CoordinationServer: (example: 127.0.0.1:3000)')
            self.config['url'] = input()
            self.config['ignore'] = {"files": ["code.zip", "CLI.py", "cli_config.json"], "folder": ["MORE-CLI"]}

        if self.config.get('experiment') is None:
            if self.config.get('project') is None:
                projects = \
                requests.request('GET', 'http://' + self.config['url'] + '/project/getAll', headers={}, files=[]).json()[
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
                        self.config['project'] = x
                        break

            if self.config.get('type') is None:
                questions = [
                    inquirer.List(
                        "type",
                        message="Choose an Experiment-Type?",
                        choices=['Trial', 'Optimization'],
                    ),
                ]

                answers = inquirer.prompt(questions)
                self.config['type'] = answers['type']
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
                    self.config['optimization'] = opti

            # Parameter
            if self.config.get('parameter') is None and self.config.get('optimization') is None:
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
                        self.config['parameter'] = tmp
                        break

            if self.config.get('parameter') is None and self.config.get('optimization') is not None:
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
                        self.config['parameter'] = tmp
                        break
            # Versions-nummer
            versions = \
                requests.request('GET',
                                 'http://' + self.config['url'] + '/project/VersionCodes?project_name=' + self.config['project'][
                                     'name'],
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
                self.config['version'] = answer['version']
            else:
                print('Set Version: (>' + max(versions) + ')')
                self.config['version'] = input()

            requirements = self.zip_directory(os.getcwd(), os.getcwd() + '/code.zip')
            self.config['requirements'] = requirements

            with open('cli_config.json', 'w') as r:
                json.dump(self.config, r)

            if self.config.get('optimization') is not None:
                payload = {
                    'optimization': {'direction': self.config['optimization']['direction'],
                                     'n_agents': self.config['optimization']['agents'],
                                     'trials': self.config['optimization']['trials']},
                    'requirements': self.config['requirements'], 'version': self.config['version']}
                payload['parameterranges'] = self.config['parameter']
                if aw == 'y' or aw == 'Y':
                    files = []
                else:
                    files = [('file', ('code.zip', open(os.getcwd() + '/code.zip', 'rb'), 'application/zip'))]
                headers = {}

                response = requests.request("POST",
                                            'http://' + self.config['url'] + '/project/createOptimization?project_id=' +
                                            self.config['project']['_id'],
                                            headers=headers,
                                            data={'experiment': json.dumps(payload)}, files=files)
                exp = response.json()['experiment']
            else:
                payload = {'requirements': self.config['requirements'], 'version': self.config['version']}
                payload['parametervalues'] = self.config['parameter']
                if aw == 'y' or aw == 'Y':
                    files = []
                else:
                    files = [('file', ('code.zip', open(os.getcwd() + '/code.zip', 'rb'), 'application/zip'))]
                headers = {}

                response = requests.request("POST",
                                            'http://' + self.config['url'] + '/project/createTrial?project_id=' +
                                            self.config['project'][
                                                '_id'],
                                            headers=headers,
                                            files=files, data={"experiment": json.dumps(payload)})
                exp = response.json()['experiment']

            self.config['experiment'] = exp
            print('Experiment has been created \u001b[32m successfully! \u001b[0m \n\r')

        print('Do you want to start the Experiment? [y/n]')
        choice = input()
        if self.config.get('notification') is None:
            print('Set an email address for notifications or press Enter:')
            email = input()
            if email != '':
                self.config['notification'] = email
        if self.config.get('notification') is not None:
            requests.request("PUT",
                             'http://' + self.config['url'] + '/project/putExperiment?exp_id=' + self.config['experiment']['_id'],
                             headers={}, data={"notification": self.config['notification']})
        if choice == 'y' or choice == 'Y':
            workstations = \
            requests.request('GET', 'http://' + self.config['url'] + '/workstation/getAllWorkstations').json()[
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
            if self.config['type'] == 'Trial':
                print('Start to prepare the Python-Environment...')
                requests.request('POST',
                                 'http://' + self.config[
                                     'url'] + '/workstation/checkRequirements?project_id={}&workstation={}&env={}&exp_no={}'.format(
                                     self.config['project']['_id'],
                                     workstation_id, self.config['project']['env'], self.config['experiment']['no']),
                                 data={})
                print('Python-Environment has been prepared \u001b[32m successfully! \u001b[0m \n\r')
                print('Execute Trial...')
                response = requests.request('POST',
                                            'http://' + self.config['url'] + '/workstation/executeTrial?project_id=' +
                                            self.config['project']['_id'] + '&exp_id=' + self.config['experiment'][
                                                '_id'] + '&workstation=' + workstation_id)
                print('Experiment has been started \u001b[32m successfully! \u001b[0m')
                print('Press Enter to finish...')
                input()
            else:
                print('Start to prepare the Python-Environment...')
                requests.request('POST', 'http://' + self.config[
                    'url'] + '/workstation/checkRequirements?project_id={}&workstation={}&env={}&exp_no={}'.format(
                    self.config['project']['_id'],
                    workstation_id, self.config['project']['env'], self.config['experiment']['no']),
                                 data={})
                print('Python-Environment has been prepared \u001b[32m successfully! \u001b[0m \n\r')
                print('Execute Optimization...')
                response = requests.request('POST',
                                            'http://' + self.config['url'] + '/workstation/executeOptimization?project_id=' +
                                            self.config['project']['_id'] + '&exp_id=' +
                                            self.config['experiment']['_id'] + '&workstation=' + workstation_id)
                print('Experiment has been started \u001b[32m successfully! \u001b[0m')
                print('Press Enter to finish...')
                input()

def main():
    if os.path.exists(os.getcwd()+'/main.py') or os.path.exists(os.getcwd()+'\main.py') or os.path.exists(os.getcwd()+'/optimize.py') or os.path.exists(os.getcwd()+'\optimize.py'):
        if platform.system() == 'Windows':
            CLIWindows()
        elif platform.system() == 'Darwin' or platform.system() == 'Linux':
            CLI()
    else:
        raise FileNotFoundError('Could not found a main.py or optimize.py file. Please navigate to a prepared project.')
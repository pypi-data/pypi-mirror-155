import platform
from CLI import CLI
from CLIWindows import CLIWindows

def main():
    if platform.system() == 'Windows':
        CLIWindows()
    elif platform.system() == 'Darwin' or platform.system() == 'Linux':
        CLI()

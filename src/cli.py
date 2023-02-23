import os, sys
import argparse
import logging
import requests

class Cli:
    CLI_VERSION = 'CLI 0.1.1'
    DEV_NAME = 'Rafael Camargo'
    DEV_EMAIL = 'rafaelcamargo.inf@gmail.com'

    GITIGONE_API = 'https://www.toptal.com/developers/gitignore/api/'
    LICENSE_API = 'https://api.github.com/licenses/'

    def __init__(self):
        self.logger = logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='cli.log')
        self.start()

    def createReadme(self, path):
        try:
            with open(os.path.join(path, 'README.md'), 'w') as readme:
                readme.write('# PROJECT README')
        except Exception as e:
            logging.error('Error creating README.md file: {}'.format(e))

    def createLicense(self, name, path):
        try:
            r = requests.get(self.LICENSE_API + name)
            if r.status_code == 200:
                with open(os.path.join(path, 'LICENSE'), 'w') as license:
                    license.write(r.json()['body'])
                logging.info('License file created: {}'.format(r.status_code))
        except Exception as e:
            logging.error('Error creating license file: {}'.format(e))

    def initGit(self, path):
        try:
            out = os.system('git init {}'.format(path))
            logging.info('Git repository initialized: {}'.format(out))
        except Exception as e:
            logging.error('Error initializing git repository: {}'.format(e))

    def createGitIgnore(self, lang, path):
        try:
            out = os.system('curl -L -o {} {}'.format(os.path.join(path, '.gitignore'), self.GITIGONE_API + lang))
            logging.info('Gitignore file created: {}'.format(out))
        except Exception as e:
            logging.error('Error creating gitignore file: {}'.format(e))

    def createGitAttributes(self, path):
        try:
            with open(os.path.join(path, '.gitattributes'), 'w') as gitattributes:
                gitattributes.write('* text=auto')
            logging.info('Gitattributes file created')
        except Exception as e:
            logging.error('Error creating gitattributes file: {}'.format(e))

    def createProject(self, name, path):
        try:
            if not os.path.exists(path):
                os.mkdir(path)
            out = os.system('mkdir {}'.format(os.path.join(path, name)))
            logging.info('Project created: {}'.format(out))
        except Exception as e:
            logging.error('Error creating project: {}'.format(e))

    def createDefFolders(self, path):
        try:
            folders = [
                'src',
                'tests',
                'docs',
                'tmp',
                'dist'
            ]
            
            if not os.path.exists(path):
                os.mkdir(path)
            
            for folder in folders:
                out = os.system('mkdir {}'.format(os.path.join(path, folder)))
                logging.info('Folder created: {}'.format(out))
        except Exception as e:
            logging.error('Error creating default folders: {}'.format(e))

    def start(self):
        self.parser = argparse.ArgumentParser(
            prog='Project CLI',
            description='Automation for creating projects',
            epilog='Developed by: {} - {}'.format(self.DEV_NAME, self.DEV_EMAIL),
            usage='%(prog)s [options]',
        )
        
        self.parser.version = self.CLI_VERSION
        self.parser.add_argument('-v', '--version', action='version', help='Show the version of the program')
        
        self.parser.add_argument('-p', '--path', action='store', help='Set the path of the project', type=str, default='.')
        
        self.parser.add_argument('-r', '--readme', action='store_true', help='Create the README.md file')
        
        self.parser.add_argument('-l', '--license', action='store', help='Create the LICENSE file', type=str)
        
        self.parser.add_argument('-g', '--git', action='store_true', help='Initialize the git repository')
        
        self.parser.add_argument('-gi', '--gitignore', action='store', help='Create the .gitignore file', type=str)
        
        self.parser.add_argument('-ga', '--gitattributes', action='store_true', help='Create the .gitattributes file')
        
        self.parser.add_argument('-c', '--create', action='store', help='Create a project', type=str)
        
        self.parser.add_argument('-df', '--default_folders', action='store_true', help='Create the default folders')
        
        if len(sys.argv) == 1:
            self.parser.print_help(sys.stderr)
            sys.exit(1)
        
        parseArgs = self.parser.parse_args()
        
        # Map the functions to the arguments
        FUNCTION_MAP = {
            'readme': self.createReadme,
            'license': self.createLicense,
            'git': self.initGit,
            'gitignore': self.createGitIgnore,
            'gitattributes': self.createGitAttributes,
            'create': self.createProject,
            'default_folders': self.createDefFolders
        }
        
        path = parseArgs.path
        
        for key, value in vars(parseArgs).items():  
            if value == True and key in FUNCTION_MAP:
                FUNCTION_MAP[key](path)
            elif value == True and key == 'default_folders' and key in FUNCTION_MAP:
                FUNCTION_MAP[key](path)
            elif key == 'license' or key == 'gitignore' or key == 'create' and key in FUNCTION_MAP:
                FUNCTION_MAP[key](value, path)
        
        print(parseArgs)

if __name__ == '__main__':
    Cli()
from support.getToken import *
from support.configCheck import *
import sys, inspect, os

def load_config(jamfSearchConfig):
    global data
    global apiUser
    global apiToken
    global baseAPIURL
    global theURL
    try:
        with open(jamfSearchConfig, 'r') as f:
            data = json.load(f)
            apiUser = data['apiUserName']
            baseAPIURL = data['jamfAPIURL']
            try:
                apiToken = keyring.get_password(baseAPIURL, apiUser+'API')
                # print(f'[>jamfAuth] Loaded API Token')
            except Exception as errorMessage:
                print(f'[ERROR>jamfAuth] {errorMessage}')
            theURL = baseAPIURL+'auth'
    except Exception as errorMessage:
        print(f'ERROR load_config: Load Config] - {errorMessage}')

def header(instance=""):
    jamfAuthPath = os.path.abspath(inspect.getfile(startAuth))
    jamfAuthPath = jamfAuthPath.strip('__init__.py')
    if instance == "dev":
        jamfSearchConfig = jamfAuthPath+'support/.jamfauth-dev.json'
    else:
        jamfSearchConfig = jamfAuthPath+'support/.jamfauth.json'

    authHeader = '''   _                  __   _         _   _     
  (_) __ _ _ __ ___  / _| /_\  _   _| |_| |__  
  | |/ _` | '_ ` _ \| |_ //_\\\| | | | __| '_ \ 
  | | (_| | | | | | |  _/  _  \ |_| | |_| | | |
 _/ |\__,_|_| |_| |_|_| \_/ \_/\__,_|\__|_| |_|
|__/ ------ jamfAuth.py (v0.3.4)[pip]
----------- josh.harvey@jamf.com
----------- Created: 04/25/22
----------- Modified: 06/16/22     
 '''

    print(authHeader)
    print(f'> jamfAuth Config Path: {jamfSearchConfig}')   


def reset_config(instance=""):
    global jamfSearchConfig
    jamfAuthPath = os.path.abspath(inspect.getfile(startAuth))
    jamfAuthPath = jamfAuthPath.strip('__init__.py')
    if instance == "dev":
        jamfSearchConfig = jamfAuthPath+'support/.jamfauth-dev.json'
    else:
        jamfSearchConfig = jamfAuthPath+'support/.jamfauth.json'

    data = {
        'apiUserName' : '',
        'jamfHostName' : '',
        'jamfAPIURL' : ''
    }

    with open(jamfSearchConfig, 'w') as output:
        json.dump(data, output)

def startAuth(instance=""):
    header(instance)
    pwd = os.getcwd()
    global jamfSearchConfig
    jamfAuthPath = os.path.abspath(inspect.getfile(startAuth))
    jamfAuthPath = jamfAuthPath.strip('__init__.py')
    ## adding dev server support
    if instance == "dev":
        jamfSearchConfig = jamfAuthPath+'support/.jamfauth-dev.json'
    else:
        jamfSearchConfig = jamfAuthPath+'support/.jamfauth.json'
    if not os.path.exists(jamfAuthPath+'support/'):
        os.makedirs(jamfAuthPath+'support/')
    
    check_config(jamfSearchConfig)
    start_config_check(jamfSearchConfig)
    load_config(jamfSearchConfig)
    check_token(apiUser, apiToken, theURL, baseAPIURL, jamfSearchConfig)
    load_config(jamfSearchConfig)
    return apiToken

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'reset':
            print('[>jamfAuth]: Resetting Settings for Production..')
            reset_config()
        if sys.argv[1] == 'reset-dev':
            print('[>jamfAuth]: Resetting Settings for Dev..')
            reset_config("dev")
        if sys.argv[1] == 'setup':
            print('[>jamfAuth]: Setting up Config for Production..')
            startAuth()
        if sys.argv[1] == 'setup-dev':
            print('[>jamfAuth]: Setting up Config for Dev..')
            startAuth("dev")
    else:
        print('no arg')
        startAuth()

if __name__ == '__main__':
    main()
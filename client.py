from utils.Authentication import Auth
from utils.ApiWrapper import ApiWrapper

import json

config = json.load(open('config.json'))

auth = Auth.get_access_token(
    cookies = Auth.get_new_cookies(),
    username = config['username'],
    password = config['password']
)

if auth['type'] == '2fa':
    print(f'Code sent to {auth["data"]["email"]}...')
    userinput:int = input('2fa code => ')
    auth = Auth.give_2fa_code(
        cookies = auth['cookies'],
        code = userinput
    )

access_token = auth['data']['access_token']
id_token = auth['data']['id_token']
entitlements_token = Auth.get_entitlements_token(access_token)
puuid = Auth.get_userinfo(access_token)['puuid']
region = Auth.get_region(access_token, id_token)

ApiWrapperClient = ApiWrapper(
    access_token,
    entitlements_token,
    puuid,
    region
)

directory = 'temp\\output.json'
endpoint = ApiWrapperClient

with open(directory, 'w+') as file:
    file.write(json.dumps(endpoint, indent=4))
print(f'Wrote output to \'{directory}\'...')
import re

from utils.req.TLSAdapter import TLSAdapter
from requests.cookies import RequestsCookieJar
import requests

DEFAULT_HEADERS = {'Accept-Language' : 'en-US,en;q=0.9'}
RIOTCLIENT_USERAGENT = 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)'

class Auth():
    def get_new_cookies() -> RequestsCookieJar:
        ''' Get new cookies for 'auth.riotgames.com' '''
        session = requests.session()
        session.headers = DEFAULT_HEADERS
        session.mount('https://', TLSAdapter())

        data = {
            'client_id': 'play-valorant-web-prod',
            'nonce': '1',
            'redirect_uri': 'https://playvalorant.com/opt_in',
            'response_type': 'token id_token',
            'scope': 'account openid'
        }

        response = session.post(f'https://auth.riotgames.com/api/v1/authorization', json=data)
        response.raise_for_status()

        return response.cookies

    def reauth(cookies:RequestsCookieJar) -> RequestsCookieJar:
        ''' Reauth the cookie and get the output of '.get_access_token()' '''
        session = requests.session()
        session.headers = DEFAULT_HEADERS
        session.mount('https://', TLSAdapter())

        data = {
            'client_id': 'play-valorant-web-prod',
            'nonce': '1',
            'redirect_uri': 'https://playvalorant.com/opt_in',
            'response_type': 'token id_token',
            'scope': 'account openid'
        }

        response = session.post(f'https://auth.riotgames.com/api/v1/authorization', json=data, cookies=cookies)
        response.raise_for_status()

        json = response.json()
        pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
        data = pattern.findall(json['response']['parameters']['uri'])[0]
        return {'type':'default', 'cookies':response.cookies, 'data':{'access_token':data[0], 'id_token':data[1]}}

    def get_access_token(username:str, password:str, cookies:RequestsCookieJar) -> dict:
        ''' Get the access token, auth type and cookie '''
        session = requests.session()
        session.headers = DEFAULT_HEADERS
        session.mount('https://', TLSAdapter())

        data = {
            'type': 'auth',
            'username': username,
            'password': password,
            'remember': True
        }

        response = session.put(f'https://auth.riotgames.com/api/v1/authorization', json=data, cookies=cookies)
        response.raise_for_status()

        json = response.json()
        if json['type'] == 'response':
            pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
            data = pattern.findall(json['response']['parameters']['uri'])[0]
            return {'type':'default', 'cookies':response.cookies, 'data':{'access_token':data[0], 'id_token':data[1]}}

        if json['type'] == 'multifactor':
            return {'type':'2fa', 'cookies':response.cookies, 'data':{'email':json['multifactor']['email']}}

        if json['type'] == 'auth':
            return {'type':'error', 'cookies':response.cookies}

    def give_2fa_code(cookies:RequestsCookieJar, code:int) -> dict:
        ''' Identical request from '.get_access_token()' only with 2fa code '''
        session = requests.session()
        session.headers = DEFAULT_HEADERS
        session.mount('https://', TLSAdapter())

        data = {
            'type': 'multifactor',
            'code': code,
            'rememberDevice': True
        }

        response = session.put(f'https://auth.riotgames.com/api/v1/authorization', json=data, cookies=cookies)
        response.raise_for_status()

        json = response.json()
        if json['type'] == 'response':
            pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
            data = pattern.findall(json['response']['parameters']['uri'])[0]
            return {'type':'default', 'cookies':response.cookies, 'data':{'access_token':data[0], 'id_token':data[1]}}

        if json['type'] == 'multifactor':
            return {'type':'error', 'cookies':response.cookies}

    def get_entitlements_token(access_token:str) -> str:
        ''' Get the entitlements_token '''
        session = requests.session()
        session.mount('https://', TLSAdapter())

        headers = {
            'User-Agent': RIOTCLIENT_USERAGENT,
            'Authorization': f'Bearer {access_token}'
        }

        response = session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={})
        response.raise_for_status()

        return response.json()['entitlements_token']

    def get_userinfo(access_token:str) -> dict:
        ''' Get the puuid and display name '''
        session = requests.session()
        session.mount('https://', TLSAdapter())

        headers = {
            'User-Agent': RIOTCLIENT_USERAGENT,
            'Authorization': f'Bearer {access_token}'
        }

        response = session.post('https://auth.riotgames.com/userinfo', headers=headers, json={})
        response.raise_for_status()

        json = response.json()
        return {'puuid':json['sub'], 'riot_id':json['acct']['game_name'], 'tagline':json['acct']['tag_line'], 'country':json['country']}

    def get_region(access_token:str, id_token:str) -> str:
        ''' Get the region. '''
        session = requests.session()
        session.mount('https://', TLSAdapter())

        headers = {
            'User-Agent': RIOTCLIENT_USERAGENT,
            'Authorization': f'Bearer {access_token}'
        }

        data = {'id_token': id_token}

        response = session.put('https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant', headers=headers, json=data)
        response.raise_for_status()

        return response.json()['affinities']['live']

if __name__ == '__main__':
    auth = Auth.get_access_token(
        cookies = Auth.get_new_cookies(),
        username = '',
        password = ''
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
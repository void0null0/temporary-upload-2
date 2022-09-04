from utils.api.ValorantApi import ValorantApi

import requests

class PvpApi():
    def __init__(self, access_token:str, entitlements_token:str, puuid:str, region:str) -> None:
        self.headers = {
            'X-Riot-Entitlements-JWT' : entitlements_token,
            'Authorization' : f'Bearer {access_token}',
            'X-Riot-ClientVersion' : ValorantApi.get_current_client_version(),
            'X-Riot-ClientPlatform' : 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9'
        }
        self.pd = f'https://pd.{region}.a.pvp.net'
        self.glz = f'https://glz-{region}-1.{region}.a.pvp.net'
        self.shared = f'https://shared.{region}.a.pvp.net'
        self.puuid = puuid

    # general
    def get_content(self):
        response = requests.get(f'{self.shared}/content-service/v3/content', headers=self.headers)
        return response.json()

    def get_xp(self):
        response = requests.get(f'{self.pd}/account-xp/v1/players/{self.puuid}', headers=self.headers)
        return response.json()

    def get_restrictions(self):
        response = requests.get(f'{self.pd}/restrictions/v3/penalties', headers=self.headers)
        return response.json()['Penalties']

    # contracts
    def get_contracts(self):
        response = requests.get(f'{self.pd}/contracts/v1/contracts/{self.puuid}', headers=self.headers)
        return response.json()

    def get_item_upgrades(self):
        response = requests.get(f'{self.pd}/contract-definitions/v3/item-upgrades', headers=self.headers)
        return response.json()['Definitions']

    # mmr
    def get_mmr(self):
        response = requests.get(f'{self.pd}/mmr/v1/players/{self.puuid}', headers=self.headers)
        return response.json()

    # personalization
    def get_playerloadout(self):
        response = requests.get(f'{self.pd}/personalization/v2/players/{self.puuid}/playerloadout', headers=self.headers)
        return response.json()

    # match
    def get_match_history(self, type:str=None, endIndex:int=10):
        params = {'endIndex' : {endIndex}}
        if type != None:
            params.update({'queue' : type})
        response = requests.get(f'{self.pd}/match-history/v1/history/{self.puuid}', params=params, headers=self.headers)
        return response.json()

    def get_competitiveupdates(self, type:str=None, endIndex:int=10):
        params = {'endIndex' : {endIndex}}
        if type != None:
            params.update({'queue' : type})
        response = requests.get(f'{self.pd}/mmr/v1/players/{self.puuid}/competitiveupdates', params=params, headers=self.headers)
        return response.json()

    def get_match_details(self, matchId:str):
        response = requests.get(f'{self.pd}/match-details/v1/matches/{matchId}', headers=self.headers)
        return response.json()

    # store
    def get_wallet(self):
        response = requests.get(f'{self.pd}/store/v1/wallet/{self.puuid}', headers=self.headers)
        return response.json()['Balances']

    def get_store_offers(self):
        response = requests.get(f'{self.pd}/store/v1/offers/', headers=self.headers)
        return response.json()

    def get_store_front(self):
        response = requests.get(f'{self.pd}/store/v2/storefront/{self.puuid}', headers=self.headers)
        return response.json()

    def get_entitlements(self, itemType:str):
        '''
            01bb38e1-da47-4e6a-9b3d-945fe4655707    Agents          ValorantApi.get_agents()
            f85cb6f7-33e5-4dc8-b609-ec7212301948    Contracts       ValorantApi.get_contracts()
            d5f120f8-ff8c-4aac-92ea-f2b5acbe9475    Sprays          ValorantApi.get_sprays()
            dd3bf334-87f3-40bd-b043-682a57a8dc3a    Buddies         ValorantApi.get_buddies()
            3f296c07-64c3-494c-923b-fe692a4fa1bd    Cards           ValorantApi.get_cards()
            e7c63390-eda7-46e0-bb7a-a6abdacd2433    Skins           ValorantApi.get_weaponskinchromas()
            3ad1b2b2-acdb-4524-852f-954a76ddae0a    Skin Variants   ValorantApi.get_weaponskinlevels()
            de7caa6b-adf7-4588-bbd1-143831e786c6    Titles          ValorantApi.get_titles()
        '''
        response = requests.get(f'{self.pd}/store/v2/storefront/{self.puuid}/{itemType}', headers=self.headers)
        return response.json()

    # status
    def get_status_party(self):
        response = requests.get(f'{self.glz}/parties/v1/players/{self.puuid}', headers=self.headers)
        return 200 >= response.status_code

    def get_status_pregame(self):
        response = requests.get(f'{self.glz}/pregame/v1/players/{self.puuid}', headers=self.headers)
        return 200 >= response.status_code

    def get_status_game(self):
        response = requests.get(f'{self.glz}/core-game/v1/players/{self.puuid}', headers=self.headers)
        return 200 >= response.status_code
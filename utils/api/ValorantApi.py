import requests

class ValorantApi():
    url = 'https://valorant-api.com/v1'

    @classmethod
    def get_current_client_version(cls) -> str:
        response = requests.get(f'{cls.url}/version')
        return response.json()['data']['riotClientVersion']

    @classmethod
    def get_levelborders(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/levelborders').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_currency(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/currencies').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_missions(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/missions').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_contracts(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/contracts').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_competitivetiers(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/competitivetiers').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_competitiveseasons(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/seasons/competitive').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_agents(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/agents?isPlayableCharacter=true').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_weapons(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/weapons').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_weaponskins(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/weapons/skins').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_weaponskinchromas(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/weapons/skinchromas').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_weaponskinlevels(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/weapons/skinlevels').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_sprays(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/sprays').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_buddylevels(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/buddies/levels').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_cards(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/playercards').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_titles(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/playertitles').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_contenttiers(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/contenttiers').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_themes(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/themes').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_bundles(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/bundles').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x

    @classmethod
    def get_maps(cls, uuid:str=None):
        data = requests.get(f'{cls.url}/maps').json()['data']
        if not uuid:
            return data
        if isinstance(uuid, str):
            for item in data:
                if item['uuid'] == uuid:
                    return item
        x = []
        if isinstance(uuid, list):
            for item in uuid:
                uuid = item
                for item in data:
                    if item['uuid'] == uuid:
                        x.append(item)
        return x
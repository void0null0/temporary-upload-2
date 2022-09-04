def get_item_by_uuid(uuid:str, list:list, weapon:bool=False):
    search = [item for item in list if (item['levels'][0]['uuid'] if weapon else item['uuid']) == uuid]
    return search[0] if len(search) >= 1 else {}

def build_new_cosmetic(fetched_data:dict, type:str, uuid:str):
    if type in ['e7c63390-eda7-46e0-bb7a-a6abdacd2433', 'EquippableSkinLevel']:
        item = {
            'type' : 'weapon',
            'data' : get_item_by_uuid(uuid, fetched_data['weaponskins']['data'], True)
        }
        theme = item['data']['themeUuid']
        content_tier = item['data']['contentTierUuid']
        item['data'].update({
            'theme' : get_item_by_uuid(theme, fetched_data['weaponskins']['themes']),
            'contentTier' : get_item_by_uuid(content_tier, fetched_data['weaponskins']['contentTiers'])
        })
        del theme, content_tier
        return item

    elif type in ['dd3bf334-87f3-40bd-b043-682a57a8dc3a', 'EquippableCharmLevel']:
        return {
            'type' : 'buddy',
                'data' : get_item_by_uuid(uuid, fetched_data['buddies'])
        }

    elif type in ['3f296c07-64c3-494c-923b-fe692a4fa1bd', 'PlayerCard']:
        return {
            'type' : 'card',
            'data' : get_item_by_uuid(uuid, fetched_data['cards'])
        }

    elif type in ['de7caa6b-adf7-4588-bbd1-143831e786c6', 'Title']:
        return {
            'type' : 'title',
            'data' : get_item_by_uuid(uuid, fetched_data['titles'])
        }

    elif type in ['d5f120f8-ff8c-4aac-92ea-f2b5acbe9475', 'Spray']:
        return {
            'type' : 'spray',
            'data' : get_item_by_uuid(uuid, fetched_data['sprays'])
        }

    elif type == 'Currency':
        return {
            'type' : 'currency',
            'data' : get_item_by_uuid(uuid, fetched_data['currencys'])
        }

    else:
        return {
            'type' : type.lower(),
            'data' : None
        }
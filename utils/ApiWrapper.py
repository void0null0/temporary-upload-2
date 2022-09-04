from utils.api.ValorantApi import ValorantApi
from utils.api.PvpApi import PvpApi

from utils.Necessary import build_new_cosmetic

class ApiWrapper():
    def __init__(self, access_token:str, entitlements_token:str, puuid:str, region:str) -> None:
        self.PvpApiClient = PvpApi(
            access_token,
            entitlements_token,
            puuid,
            region
        )

    def get_xp(self):
        pvpApi_xp = self.PvpApiClient.get_xp()['Progress']
        valApi_levelborders = ValorantApi.get_levelborders()
        xp = {
            'level' : pvpApi_xp['Level'],
            'xp' : pvpApi_xp['XP'],
            'xpNeededForLevel' : 5000
        }

        for item in valApi_levelborders:
            if item['startingLevel'] <= xp['level']:
                xp.update({'levelborder' : item})

        return xp

    def get_seasons(self, currentSeason:bool=True, episodes:bool=False):
        pvpApi_seasons = self.PvpApiClient.get_content()['Seasons'][::-1]
        valApi_competitiveseasons = ValorantApi.get_competitiveseasons()
        valApi_competitivetiers = ValorantApi.get_competitivetiers()

        new_seasons = []
        for i, item in enumerate(pvpApi_seasons):
            new_season = {}
            new_season.update({
                'uuid' : item['ID'],
                'parentUuid' : None,
                'type' : item['Type'],
                'name' : item['Name'],
                'isActive' : item['IsActive'],
                'startTime' : item['StartTime'],
                'endTime' : item['EndTime']
            })

            if i % 4 == 0:
                episode_name = new_season['name']
                parent_uuid = new_season['uuid']

            if new_season['type'] == 'act':
                new_season.update({
                    'name' : f'{episode_name}: {new_season["name"]}',
                    'parentUuid' : parent_uuid
                })

            for item in valApi_competitiveseasons:
                if new_season['uuid'] == item['seasonUuid']:
                    new_season.update({
                        'borders' : item['borders'],
                        'competitiveTiers' : [item2 for item2 in valApi_competitivetiers if item2['uuid'] == item['competitiveTiersUuid']]
                    })
            new_seasons.append(new_season)
        pvpApi_seasons = new_seasons

        if currentSeason:
            for item in pvpApi_seasons:
                if item['type'] == 'act' and item['isActive']:
                    return item
        if episodes == False:
            return [item for item in pvpApi_seasons if item['type'] == 'act']
        return pvpApi_seasons[::-1]

    def get_restrictions(self):
        pvpApi_restrictions = self.PvpApiClient.get_restrictions()

        data = []
        for item in pvpApi_restrictions:
            penalty = {}
            penalty.update({'expiry' : item['Expiry']})

            if item['WarningEffect'] != None:
                penalty.update({
                    'type' : 'Warning',
                    'warningType' : item['WarningEffect']['WarningType'],
                    # afk/doges = round(int/10*3)
                    'warningTier' : item['WarningEffect']['WarningTier'],
                    'gamesRemaining' : item['GamesRemaining']
                })

            elif item['QueueRestrictionEffect'] != None:
                penalty.update({'type' : 'Queue Ban'})

            elif item['GameBanEffect'] != None:
                penalty.update({'type' : 'Game Ban'})

            data.append(penalty)
        pvpApi_restrictions = data

        return [item for item in pvpApi_restrictions if len(item) != 1] if pvpApi_restrictions != [] else None

    def get_wallet(self):
        pvpApi_wallet = self.PvpApiClient.get_wallet()
        valApi_currency = ValorantApi.get_currency(list(pvpApi_wallet.keys()))
        for item in valApi_currency:
            item.update({'amount' : pvpApi_wallet[item['uuid']]})
        return valApi_currency

    def get_missions(self):
        pvpApi_missions = self.PvpApiClient.get_contracts()['Missions']
        valApi_missions = ValorantApi.get_missions([item['ID'] for item in pvpApi_missions])

        for i, item in enumerate(valApi_missions):
            item.update({
                'progress' : pvpApi_missions[i]['Objectives'][list(pvpApi_missions[i]['Objectives'].keys())[0]]
            })

        return {'Missions' : valApi_missions, 'FirstWinAvailable' : self.PvpApiClient.get_xp()['NextTimeFirstWinAvailable']}

    def get_agent_contracts(self):
        pvpApi_contracts = self.PvpApiClient.get_contracts()
        pvpApi_contracts2 = pvpApi_contracts['Contracts']
        valApi_contracts = ValorantApi.get_contracts([item['ContractDefinitionID'] for item in pvpApi_contracts2])

        fechted_data = {
            'weaponskins' : {
                'data' : ValorantApi.get_weaponskins(),
                'themes' : ValorantApi.get_themes(),
                'contentTiers' : ValorantApi.get_contenttiers()
            },
            'cards' : ValorantApi.get_cards(),
            'sprays' : ValorantApi.get_sprays(),
            'buddies' : ValorantApi.get_buddylevels(),
            'titles' : ValorantApi.get_titles()
        }

        for i, item in enumerate(valApi_contracts):
            item.update({'progression' : {
                'progressionLevelReached' : pvpApi_contracts2[i]['ProgressionLevelReached'],
                'progressionTowardsNextLevel' : pvpApi_contracts2[i]['ProgressionTowardsNextLevel'],
            }})
        agent_contracts = [item for item in valApi_contracts if item['content']['relationType'] == 'Agent']

        for agent in agent_contracts:
            for chapter in agent['content']['chapters']:
                for item in chapter['levels']:
                    new_cosmetic = build_new_cosmetic(
                        fetched_data = fechted_data,
                        type = item['reward']['type'],
                        uuid = item['reward']['uuid']
                    )
                    item.update({'reward' : new_cosmetic})

        return {'Contracts' : agent_contracts, 'ActiveContract' : pvpApi_contracts['ActiveSpecialContract']}

    # not tested
    def get_storebonus(self):
        pvpApi_storefront = self.PvpApiClient.get_store_front()
        if 'BonusStore' not in pvpApi_storefront:
            return None
        pvpApi_storefront = pvpApi_storefront['BonusStore']
        offers = pvpApi_storefront['BonusStoreOffers']

        fechted_data = {
            'weaponskins' : {
                'data' : ValorantApi.get_weaponskins(),
                'themes' : ValorantApi.get_themes(),
                'contentTiers' : ValorantApi.get_contenttiers()
            }
        }

        new_items = []
        for item in offers:
            new_item = {}
            new_cosmetic = build_new_cosmetic(
                fetched_data = fechted_data,
                type = item['Item']['ItemTypeID'],
                uuid = item['Item']['ItemID']
            )
            new_item.update({'data' : new_cosmetic})

            new_item['data'].update({
                'cost' : item['Offer']['Cost'][list(item['Offer']['Cost'].keys())[0]],
                'isSeen' : item['IsSeen'],
                'discountPercent' : item['DiscountPercent'],
                'costAfterDiscount' : item['DiscountCosts'][list(item['DiscountCosts'].keys())[0]]
            })

            new_items.append(new_item)

        pvpApi_storefront['BonusStoreOffers'] = new_items
        return pvpApi_storefront

    def get_storebundle(self):
        pvpApi_storefront = self.PvpApiClient.get_store_front()['FeaturedBundle']['Bundle']
        valApi_bundle = ValorantApi.get_bundles(pvpApi_storefront['DataAssetID'])
        offers = pvpApi_storefront['Items']
        valApi_bundle.update({'cost' : sum([item['DiscountedPrice'] for item in offers])})

        fechted_data = {
            'weaponskins' : {
                'data' : ValorantApi.get_weaponskins(),
                'themes' : ValorantApi.get_themes(),
                'contentTiers' : ValorantApi.get_contenttiers()
            },
            'cards' : ValorantApi.get_cards(),
            'sprays' : ValorantApi.get_sprays(),
            'buddies' : ValorantApi.get_buddylevels(),
            'titles' : ValorantApi.get_titles()
        }

        new_items = []
        for item in offers:
            new_item = {}
            new_cosmetic = build_new_cosmetic(
                fetched_data = fechted_data,
                type = item['Item']['ItemTypeID'],
                uuid = item['Item']['ItemID']
            )
            new_item.update({'data' : new_cosmetic})

            new_item['data'].update({
                'cost' : item['BasePrice'],
                'amount' : item['Item']['Amount'],
                'discountPercent' : item['DiscountPercent'],
                'costAfterDiscount' : item['DiscountedPrice']
            })

            new_items.append(new_item)
        offers = new_items

        return {'bundle' : valApi_bundle, 'items' : offers}

    def get_storedaily(self):
        pvpApi_storefront = self.PvpApiClient.get_store_front()['SkinsPanelLayout']['SingleItemOffers']
        pvpApi_offers = self.PvpApiClient.get_store_offers()['Offers']

        fechted_data = {
            'weaponskins' : {
                'data' : ValorantApi.get_weaponskins(),
                'themes' : ValorantApi.get_themes(),
                'contentTiers' : ValorantApi.get_contenttiers()
            }
        }

        offers = []
        for uuid in pvpApi_storefront:
            new_item = {}

            new_cosmetic = build_new_cosmetic(
            fetched_data = fechted_data,
            type = 'e7c63390-eda7-46e0-bb7a-a6abdacd2433',
            uuid = uuid
            )
            new_item.update({'data' : new_cosmetic})

            for item in pvpApi_offers:
                if uuid == item['OfferID']:
                    new_item['data'].update({'cost' : item['Cost'][list(item['Cost'].keys())[0]]})

            offers.append(new_item)
        return offers

    def get_status(self):
        pvpApi_party = self.PvpApiClient.get_status_party()
        pvpApi_pregame = self.PvpApiClient.get_status_pregame()
        pvpApi_game = self.PvpApiClient.get_status_game()

        if not pvpApi_party:
            return {'status' : None}
        if pvpApi_pregame:
            return {'status' : 'pregame'}
        if pvpApi_game:
            return {'status' : 'game'}
        return {'status' : 'lobby'}

    def get_mmr(self, seasonUuid:str=None):
        pvpApi_mmr = self.PvpApiClient.get_mmr()['QueueSkills']['competitive']
        valApi_competitivetiers = ValorantApi.get_competitivetiers()

        if pvpApi_mmr['TotalGamesNeededForRating'] != 0:
            return {'gamesNeededForRating' : pvpApi_mmr['TotalGamesNeededForRating']}

        seasons = list(pvpApi_mmr['SeasonalInfoBySeasonID'][item] for item in list(pvpApi_mmr['SeasonalInfoBySeasonID'].keys()))

        get_rank = lambda competitivetier, competitivetiers : competitivetiers[len(competitivetiers)-1]['tiers'][competitivetier]

        data = []
        for item in seasons:
            data.append({
                'uuid' : item['SeasonID'],
                'tier' : get_rank(item['CompetitiveTier'], valApi_competitivetiers),
                'rr' : item['RankedRating'],
                'gamesPlayed' : item['NumberOfGames'],
                'gamesWon' : item['NumberOfWins'],
                'WinsByTier' : item['WinsByTier']
            })
        pvpApi_mmr = data

        if seasonUuid != None:
            for item in pvpApi_mmr:
                if item['uuid'] == seasonUuid:
                    return item
        return pvpApi_mmr

    def get_match_history(self, type:str=None, endIndex:int=10):
        pvpApi_matchhistory = self.PvpApiClient.get_match_history(type=type, endIndex=endIndex)['History']
        pvpApi_competitiveupdates = self.PvpApiClient.get_competitiveupdates(type=type, endIndex=endIndex)['Matches']
        valApi_competitivetiers = ValorantApi.get_competitivetiers()
        valApi_maps = ValorantApi.get_maps()

        get_map = lambda mapUrl, maps : [item for item in maps if item['mapUrl'] == mapUrl]
        get_rank = lambda competitivetier, competitivetiers : competitivetiers[len(competitivetiers)-1]['tiers'][competitivetier]
        get_team_mvp = lambda teamId, players : max([item['stats']['score'] for item in players if item['teamId'] == teamId])

        if len(pvpApi_matchhistory) > len(pvpApi_competitiveupdates):
            for i in range(len(pvpApi_matchhistory)):
                pvpApi_competitiveupdates.append(None)

        for i, item in enumerate(pvpApi_matchhistory):
            item.update({'matchData' : self.PvpApiClient.get_match_details(item['MatchID'])})

            item['matchData']['matchInfo'].update({'mapData' : get_map(item['matchData']['matchInfo']['mapId'], valApi_maps)})
            del item['matchData']['matchInfo']['mapId']

            players = item['matchData']['players']

            if item['matchData']['matchInfo']['gameMode'] != '/Game/GameModes/Deathmatch/DeathmatchGameMode.DeathmatchGameMode_C':
                team_red_mvp_score = get_team_mvp('Red', players)
                team_blue_mvp_score = get_team_mvp('Blue', players)
                match_mvp_score = max([item['stats']['score'] for item in players])

                for player in players:
                    player.update({
                        'matchMvp' : match_mvp_score == player['stats']['score'],
                        'teamMvp' : False
                    })
                    if player['teamId'] == 'Red':
                        player.update({'teamMvp' : team_red_mvp_score == player['stats']['score']})
                    elif player['teamId'] == 'Blue':
                        player.update({'teamMvp' : team_blue_mvp_score == player['stats']['score']})

            if pvpApi_competitiveupdates[i] == None:
                continue
            if item['QueueID'] == 'competitive':
                item.update({
                    'tierAfterUpdate' : get_rank(pvpApi_competitiveupdates[i]['TierAfterUpdate'], valApi_competitivetiers),
    			    'tierBeforeUpdate' : get_rank(pvpApi_competitiveupdates[i]['TierBeforeUpdate'], valApi_competitivetiers),
                    'rrReceived' : pvpApi_competitiveupdates[i]['RankedRatingEarned'],
                    'rrPerformanceBonus' : pvpApi_competitiveupdates[i]['RankedRatingPerformanceBonus'],
                })

        return pvpApi_matchhistory

    def get_battlepass(self, seasonUuid:str=None):
        pvpApi_contracts = self.PvpApiClient.get_contracts()['Contracts']
        pvpApi_contracts = [item for item in pvpApi_contracts if len(item['ContractProgression']['HighestRewardedLevel']) == 2]
        valApi_contracts = ValorantApi.get_contracts([item['ContractDefinitionID'] for item in pvpApi_contracts])

        fechted_data = {
            'weaponskins' : {
                'data' : ValorantApi.get_weaponskins(),
                'themes' : ValorantApi.get_themes(),
                'contentTiers' : ValorantApi.get_contenttiers()
            },
            'cards' : ValorantApi.get_cards(),
            'sprays' : ValorantApi.get_sprays(),
            'buddies' : ValorantApi.get_buddylevels(),
            'titles' : ValorantApi.get_titles(),
            'currencys' : ValorantApi.get_currency()
        }

        for i, item in enumerate(valApi_contracts):
            HighestRewardedLevel = pvpApi_contracts[i]['ContractProgression']['HighestRewardedLevel']
            item.update({
                'premiumActive' : HighestRewardedLevel[list(HighestRewardedLevel.keys())[1]] != 0,
                'progressionLevelReached' : pvpApi_contracts[i]['ProgressionLevelReached'],
                'progressionTowardsNextLevel' : pvpApi_contracts[i]['ProgressionTowardsNextLevel'],
            })

        for battlepass in valApi_contracts:
            for chapter in battlepass['content']['chapters']:
                for item in chapter['levels']:
                    new_cosmetic = build_new_cosmetic(
                        fetched_data = fechted_data,
                        type = item['reward']['type'],
                        uuid = item['reward']['uuid']
                    )
                    item.update({'reward' : new_cosmetic})

                if chapter['freeRewards'] != None:
                    for item in chapter['freeRewards']:
                        new_cosmetic = build_new_cosmetic(
                            fetched_data = fechted_data,
                            type = item['type'],
                            uuid = item['uuid']
                        )
                        item.update({'reward' : new_cosmetic})

        if seasonUuid != None:
            for item in valApi_contracts:
                if item['content']['relationUuid'] == seasonUuid:
                    return item
        return valApi_contracts
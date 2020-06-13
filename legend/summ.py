'''
Main Summoner file for League Project

Created to fetch data from Riot API
and create a dict containing data from
League of Legends profile

Utilizes Django, Riot API, and Riot Watcher Library

'''
from riotwatcher import LolWatcher, ApiError
import os
RIOT_API_KEY = os.environ['RIOT_API_KEY']
r = LolWatcher(RIOT_API_KEY)
'''
Various functions that when called retrieve and return data on user


'''

class Summoner:

    def __init__(self, name, region):
        self.name = name
        self.region = region
        self.info = r.summoner.by_name(region, name)
        self.id = self.info['id']
        self.profileIconId = str(self.info['profileIconId'])
        
        self.version = (r.data_dragon.versions_for_region(region))['n']
        self.champList = (r.data_dragon.champions(self.version['champion']))['data']


    def profileData(self):
        proIconURL = 'http://ddragon.leagueoflegends.com/cdn/' + self.version['profileicon'] + '/img/profileicon/' + str(self.profileIconId) + '.png'

        profileData = {
            'proName': self.info['name'],
            'proLevel': self.info['summonerLevel'],
            'proIconURL': proIconURL
        }
        return profileData


    def getMastery(self):
        mastery_list = []
        mastery_data = r.champion_mastery.by_summoner(self.region, self.id)

        def getChampName(self, champKey):
            for x in self.champList:
                if self.champList[x]['key'] == champKey:
                    return x

        def getChampIconURL(self, champName):
            champURL = 'http://ddragon.leagueoflegends.com/cdn/' + self.version['champion'] + '/img/champion/' + champName + '.png'
            return champURL

        for i in range(3):
            champKey = str(mastery_data[i]['championId'])
            champName = getChampName(self, champKey)
            champIconURL = getChampIconURL(self, champName)
            mastery_set = {
                'champName': champName,
                'champIconURL': champIconURL,
                'masteryLevel': mastery_data[i]['championLevel'],
                'masteryPoints': mastery_data[i]['championPoints']
            }
            mastery_list.append(mastery_set)
        return mastery_list


#p = Summoner('koalth', 'na1')
#print(p.getMastery())
#print(p.profileData())

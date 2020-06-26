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


Todo:
    1. Add items to the match history, need more data to display for each match
    2. Comment code through project, explaining each method of the Summoner class, as well as JSON data
    3. Clean up website UI / clean up code
    4. Finish README with description and demo

'''

class Summoner:

    def __init__(self, name, region):
        self.name = name
        self.region = region
        self.info = r.summoner.by_name(region, name)
        self.id = self.info['id']
        self.accountId = self.info['accountId']
        self.profileIconId = str(self.info['profileIconId'])
        
        self.version = (r.data_dragon.versions_for_region(region))['n']
        self.champList = (r.data_dragon.champions(self.version['champion']))['data']


    '''
    profileData

    returns dict containing user's profile name, profile level, and profile icon URL

    @Params self

    @Return dict

    '''
    def profileData(self):
        proIconURL = 'http://ddragon.leagueoflegends.com/cdn/' + self.version['profileicon'] + '/img/profileicon/' + str(self.profileIconId) + '.png'

        profileData = {
            'proName': self.info['name'],
            'proLevel': self.info['summonerLevel'],
            'proIconURL': proIconURL
        }
        return profileData



    def getChampName(self, champKey):
            for x in self.champList:
                if self.champList[x]['key'] == champKey:
                    return x

    def getChampIconURL(self, champName):
            champURL = 'http://ddragon.leagueoflegends.com/cdn/' + self.version['champion'] + '/img/champion/' + champName + '.png'
            return champURL

    def getMastery(self):
        mastery_list = []
        mastery_data = r.champion_mastery.by_summoner(self.region, self.id)
        '''
        def getChampName(self, champKey):
            for x in self.champList:
                if self.champList[x]['key'] == champKey:
                    return x
        '''

        '''
        def getChampIconURL(self, champName):
            champURL = 'http://ddragon.leagueoflegends.com/cdn/' + self.version['champion'] + '/img/champion/' + champName + '.png'
            return champURL
        '''
        for i in range(3):
            champKey = str(mastery_data[i]['championId'])
            champName = self.getChampName(champKey)
            champIconURL = self.getChampIconURL(champName)
            mastery_set = {
                'champName': champName,
                'champIconURL': champIconURL,
                'masteryLevel': mastery_data[i]['championLevel'],
                'masteryPoints': mastery_data[i]['championPoints']
            }
            mastery_list.append(mastery_set)
        return mastery_list

    def getMatchHistory(self):
        match_history_by_id = []
        matchHistory = r.match.matchlist_by_account(self.region, self.accountId)
        for x in matchHistory['matches']:
            match_history_by_id.append(x['gameId'])
        return match_history_by_id

    def getMatchDetails(self, matchId):
        '''
        def getChampName(self, champKey):
            for x in self.champList:
                if self.champList[x]['key'] == champKey:
                    return x
        '''
        match_data = r.match.by_id(self.region, matchId)
        for i in range(10):
            if match_data['participantIdentities'][i]['player']['accountId'] == p.accountId:
                participantId = match_data['participantIdentities'][i]['participantId']
        for i in range(10):
            if match_data['participants'][i]['participantId'] == participantId:
                sumData = match_data['participants'][i]
                sumChamp = sumData['championId']
                sumKill = sumData['stats']['kills']
                sumDeaths = sumData['stats']['deaths']
                sumAssists = sumData['stats']['assists']
                sumTeam = sumData['teamId']
        for i in range(2):
            if(match_data['teams'][i]['teamId']) == sumTeam:
                win_lose = match_data['teams'][i]['win']
        
        sumChampName = self.getChampName(str(sumChamp))
        sumChampIcon = self.getChampIconURL(sumChampName)
        match_details = {
            'sumChamp': sumChampName,
            'sumChampIconURL': sumChampIcon,
            'sumKills': sumKill,
            'sumDeaths': sumDeaths,
            'sumAssists': sumAssists,
            'win_lose' : win_lose
        }
        return match_details

    def getMatchHistory(self):
        match_history_by_id = []
        matchHistory = r.match.matchlist_by_account(self.region, self.accountId)
        #print(self.name)
        # Try 50 and see the time

        for x in range(10):
            match = matchHistory['matches'][x]
            match_history_by_id.append(match['gameId']) 
        
        '''
        for x in matchHistory['matches']:
            match_history_by_id.append(x['gameId'])
        '''

        return match_history_by_id
    
    def getMatchDetails(self, matchId):

        # Move outside of this method
        '''
        def getChampName(self, champKey):
            for x in self.champList:
                if self.champList[x]['key'] == champKey:
                    return x
        '''

        match_data = r.match.by_id(self.region, matchId)
        for i in range(10):
            if match_data['participantIdentities'][i]['player']['accountId'] == self.accountId:
                participantId = match_data['participantIdentities'][i]['participantId']
        for i in range(10):
            if match_data['participants'][i]['participantId'] == participantId:
                sumData = match_data['participants'][i]
                sumChamp = sumData['championId']
                sumKill = sumData['stats']['kills']
                sumDeaths = sumData['stats']['deaths']
                sumAssists = sumData['stats']['assists']
                sumTeam = sumData['teamId']
        for i in range(2):
            if(match_data['teams'][i]['teamId']) == sumTeam:
                win_lose = match_data['teams'][i]['win']
        
        sumChampName = self.getChampName(str(sumChamp))
        sumChampIcon = self.getChampIconURL(sumChampName)
        match_details = {
            'sumChamp': sumChampName,
            'sumChampIconURL': sumChampIcon,
            'sumKills': sumKill,
            'sumDeaths': sumDeaths,
            'sumAssists': sumAssists,
            'win_lose' : win_lose
        }
        return match_details

    def getCompleteMatchHistory(self):
        match_history = []
        sumMatchHistory = self.getMatchHistory()
        for x in sumMatchHistory:
            matchData = self.getMatchDetails(x)
            match_history.append(matchData)
        return match_history

#p = Summoner('koalth', 'na1')
#print(p.getMastery())
#print(p.profileData())
#print(p.getCompleteMatchHistory())

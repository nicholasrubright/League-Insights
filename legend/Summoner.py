from django.conf import settings
from riotwatcher import RiotWatcher, ApiError

r = RiotWatcher(settings.RIOT_API_KEY)
version = (r.data_dragon.versions_for_region('na1'))['n']['summoner']

champList = (r.data_dragon.champions(version))['data']

def getChampIcon(name):
    url = 'http://ddragon.leagueoflegends.com/cdn/' + version + '/img/champion/' + name + '.png'
    return url

def getChampName(champID):
        for i in champList:
            champ = champList[i]
            myID = champ['key']
            if myID == champID:
                return champ['id']
                break

class Summoner:

    def __init__(self, name, region):
        self.name = name
        self.region = region
        self.info = r.summoner.by_name(region, name)
        self.id = self.info['id']

    def getInfo(self):
        return self.id

    def getTopMastery(self):
        topChampID = ((r.champion_mastery.by_summoner(self.region, self.id))[0])['championId']

        name = getChampName(str(topChampID))
        return name

#p = Summoner("koalth", "na1")
#data = p.getTopMastery()
#print(data)

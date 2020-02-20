from riotwatcher import RiotWatcher, ApiError
from django.shortcuts import render
from django.conf import settings
from django.http import Http404
from legend.Summoner import Summoner
from legend.Summoner import getChampIcon
# Create your views here.

def legend_view(request):
    try:
        if request.method == 'GET':
            name = request.GET.get('name')
            region = request.GET.get('region')
            sum = Summoner(name, region)
            #sumTop = sum.getTopMastery()
            sumData = sum.getData()
            masteryList = sum.getTop3Mastery()
            #URL = getChampIcon(sumTop)
            list_dict = {
                'sumdata': sumData,
                'mastery_list': masteryList
            }
            #sumDict = {
            #    'topChampMastery': sumTop,
            #    'topChampMasteryIconURL': URL,
            #    'summonerName': name
            #}
            return render(request, 'legend.html', list_dict)
    except:
        raise Http404('Page does not exist')

from riotwatcher import RiotWatcher, ApiError
from django.shortcuts import render
from django.conf import settings
from django.http import Http404
from legend.summ import Summoner
#from legend.Summoner import Summoner
#from legend.Summoner import getChampIcon
# Create your views here.

def legend_view(request):
    try:
        if request.method == 'GET':
            name = request.GET.get('name')
            region = request.GET.get('region')
            sum = Summoner(name, region)
            sumData = sum.profileData()
            masteryData = sum.getMastery()
            matchHistory = sum.getCompleteMatchHistory()
            list_dict = {
                'sumdata': sumData,
                'masterydata': masteryData,
                'matchhistory': matchHistory,
            }
            print(list_dict)
            return render(request, 'legend.html', list_dict)
    except:
        raise Http404('Page does not exist')

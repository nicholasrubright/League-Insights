from django.shortcuts import render
from django.http import Http404

def home_view(request):
    try:
        return render(request, 'home.html')
    except:
        raise Http404('Page does not exist')

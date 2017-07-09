from django.http import Http404
from django.shortcuts import render
from .models import Beer
from .models import Brewery


# List of all beers !!!WILL NOT LOOK SAME WHEN FINISHED!!!
def index(request):
    all_beers = Beer.objects.all()
    return render(request, 'beers/index.html', {'all_beers': all_beers})


# List of all breweries
def breweries(request):
    all_breweries = Brewery.objects.all()
    return render(request, 'beers/breweries.html', {'all_breweries': all_breweries})


# Beer details
def detail(request, beer_id):
    try:
        beer = Beer.objects.get(id=beer_id)
    except Beer.DoesNotExist:
        raise Http404("Beer Does Not Exist!")
    return render(request, 'app1/detail.html', {'beer': beer})

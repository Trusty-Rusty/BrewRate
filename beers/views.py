from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Beer
from .models import Brewery


# List of all beers !!!WILL NOT LOOK SAME WHEN FINISHED!!!
def index(request):
    all_breweries = Brewery.objects.all()
    return render(request, 'beers/index.html', {'all_breweries': all_breweries})


# List of all breweries
def breweries(request):
    all_breweries = Brewery.objects.all()
    return render(request, 'beers/breweries.html', {'all_breweries': all_breweries})


# Beer details
def detail(request, brewery_id):
    brewery_id = get_object_or_404(Brewery, pk=brewery_id)
    return render(request, 'beers/detail.html', {'brewery': brewery_id})

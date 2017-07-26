from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Brewery, Beer, Style


# List of all beers !!!WILL NOT LOOK SAME WHEN FINISHED!!!
def index(request):
    all_beers = Beer.objects.all()
    return render(request, 'beers/index.html', {'all_beers': all_beers})


# User signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('beers:index')

    else:
        form = UserCreationForm()
    return render(request, 'beers/signup.html', {'form': form})


# List of all breweries
def breweries(request):
    all_breweries = Brewery.objects.all()
    return render(request, 'beers/breweries.html', {'all_breweries': all_breweries})


# Beer details
def detail(request, brewery_id):
    brewery_id = get_object_or_404(Brewery, pk=brewery_id)
    return render(request, 'beers/detail.html', {'brewery': brewery_id})

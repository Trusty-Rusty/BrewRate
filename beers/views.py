from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.views.generic import View, TemplateView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from .models import Brewery, Beer, Style


# Landing page with list of most recent beers and and invite to create user account
class MainPage(TemplateView):

    #context_object_name = 'recent_beers'
    template_name = 'beers/main.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        context['recent_beers'] = Beer.objects.all() [:5]
        return context


class BreweryDetailPage(SingleObjectMixin, ListView):
    # context_object_name = 'recent_beers'
    template_name = 'beers/brewery_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Brewery.objects.all())
        return super(BreweryDetailPage, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BreweryDetailPage, self).get_context_data(**kwargs)
        context['brewery'] = self.object
        return context

    def get_queryset(self):
        return self.object.beer_set.all()


# List of all breweries using generic included ListView
class AllBreweries(generic.ListView):
    model = Brewery
    context_object_name = 'all_breweries'
    template_name = 'beers/breweries_list.html'


# List of all Beers
class AllBeers(generic.ListView):
    model = Beer
    context_object_name = 'all_beers'
    template_name = 'beers/beer_list.html'


class BeerDetailView(generic.DetailView):
    model = Beer
    template_name = 'beers/beer_detail.html'



# -----------------------------------------------------------------------------------
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


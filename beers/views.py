from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Avg
from .forms import RatingForm
from .models import Brewery, Beer, Rating




# Landing page with list of most recent beers and and invite to create user account
class MainPage(TemplateView):

    #context_object_name = 'recent_beers'
    template_name = 'beers/main.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        context['recent_beers'] = Beer.objects.order_by('-beer_add_date') [:5]
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
class AllBreweries(ListView):
    model = Brewery
    context_object_name = 'all_breweries'
    template_name = 'beers/breweries_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(AllBreweries, self).get_context_data(**kwargs)
        context['all_breweries'] = Brewery.objects.order_by('brewery_name')
        return context


# List of all Beers
class AllBeers(ListView):
    model = Beer
    context_object_name = 'all_beers'
    template_name = 'beers/beer_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(AllBeers, self).get_context_data(**kwargs)
        all_beers = Beer.objects.order_by('beer_name')
        beer_ratings = {}
        for beer in all_beers:
            avg_rating = Rating.objects.filter(rating_beer__beer_name=beer).aggregate(Avg('rating_score')).values()[0]
            short_key = beer.beer_name
            beer_ratings[short_key] = avg_rating
        context['all_beers'] = all_beers
        context['beer_ratings'] = beer_ratings
        return context


class BeerDetailView(FormMixin, DetailView):
    model = Beer
    form_class = RatingForm

    def get_success_url(self):
        return reverse('beer_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(BeerDetailView, self).get_context_data(**kwargs)
        context['form'] = RatingForm(initial={'post': self.object.id})
        try:
            rating = Rating.objects.get(rating_user=self.request.user, rating_beer=self.object).rating_score
            context['current_rating'] = int(rating)
            int_list = []

            for i in range(context['current_rating']):
                int_list.append('x')

            context['star_rating'] = int_list

        except ObjectDoesNotExist:
            print('Beer not yet rated by the current user.')

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            rating = Rating.objects.create(rating_beer=self.object, rating_user=self.request.user, rating_score=form.cleaned_data['rating_score'])
            rating.save()
            return super(BeerDetailView, self).form_valid(form)
        else:
            return self.form_invalid(form)




        #if not request.user.is_authenticated:
         #   return HttpResponseForbidden()




class AddBeerView(CreateView):
    model = Beer
    fields = ['beer_name', 'beer_brewery', 'beer_style', 'beer_abv', 'beer_srm', 'beer_logo', 'beer_photo']


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


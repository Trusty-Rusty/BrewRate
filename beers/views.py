from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.views.generic import TemplateView, ListView, DetailView, CreateView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Avg
from django.urls import reverse_lazy
from .forms import RatingForm #UserLoginForm, BreweryForm
from .models import Beer, Brewery, Rating, User




# Landing page with list of most recent beers and and invite to create user account
class MainPage(TemplateView):

    #context_object_name = 'recent_beers'
    template_name = 'beers/main.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        context['recent_beers'] = Beer.objects.order_by('-beer_add_date') [:5]
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
        else:
            context['user'] = ''
        return context


class BreweryDetailView(SingleObjectMixin, ListView):
    template_name = 'beers/brewery_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Brewery.objects.all())
        return super(BreweryDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BreweryDetailView, self).get_context_data(**kwargs)
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
        ''' #Avg ratings abandoned on this page
        for beer in all_beers:
            avg_rating = round(Rating.objects.filter(rating_beer__beer_name=beer).aggregate(Avg('rating_score')).values()[0], 1)
            short_key = beer.id
            beer_ratings[short_key] = avg_rating
        '''
        context['all_beers'] = all_beers
        context['beer_ratings'] = beer_ratings
        return context


class BeerDetailView(FormMixin, DetailView):
    model = Beer
    form_class = RatingForm

    def get_success_url(self):
        return reverse('beers:beer_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(BeerDetailView, self).get_context_data(**kwargs)
        context['form'] = RatingForm(initial={'post': self.object.id})

        if self.request.user.is_authenticated:
            try:
                rating = Rating.objects.get(rating_user=self.request.user, rating_beer=self.object).rating_score
                context['current_rating'] = int(rating)
                int_list = []

                for i in range(context['current_rating']):
                    int_list.append('x')

                context['star_rating'] = int_list

            except ObjectDoesNotExist:
                print('Beer not yet rated by the current user.')

        else:
            context['form'] = "You must be logged in as a user to rate beers"

        context['style_beers'] = Beer.objects.filter(beer_style=self.object.beer_style).exclude(beer_name=self.object)

        if Rating.objects.filter(rating_beer__beer_name=self.object).exists():
            context['avg_rating'] = round(Rating.objects.filter(rating_beer__beer_name=self.object).aggregate(Avg('rating_score')).values()[0],1)
        else:
            context['avg_rating'] = 'Not Yet Rated'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            rating = Rating.objects.create(rating_beer=self.object, rating_user=self.request.user, rating_score=form.cleaned_data['rating_score'])
            rating.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AddBeerView(CreateView):
    model = Beer
    fields = ['beer_name', 'beer_brewery', 'beer_style', 'beer_abv', 'beer_srm', 'beer_logo', 'beer_photo']


class AddBreweryView(CreateView):
    model = Brewery
    fields = ['brewery_name', 'brewery_location', 'brewery_founding', 'brewery_logo', 'brewery_photo']


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'beers/user_detail.html'
    model = User
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['user_beers'] = Rating.objects.filter(rating_user=self.request.user)
        return context

'''
class UserLoginView(TemplateView):
    template_name = 'beers/login.html'
    form_class = UserLoginForm
'''


class UserLoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect('/form') #Why does this argument get ignored in favor of LOGIN_REDIRECT_URL?
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

        #return render(request, "beers/main.html")
'''
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)
'''
class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('beers:login')
    template_name = 'registration/signup.html'

'''
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
    return render(request, 'beers/templates/registration/signup.html', {'form': form})
'''

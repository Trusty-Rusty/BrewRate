from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import *
app_name = 'beers'

urlpatterns = [
    # /
    url(r'^$', MainPage.as_view(), name='main'),

    # /breweries/
    url(r'^breweries$', AllBreweries.as_view(), name='breweries'),

    # /beers/
    url(r'^beers$', AllBeers.as_view(), name='beers'),

    # beers/123/
    url(r'^beers/(?P<pk>[0-9]+)/$', BeerDetailView.as_view(), name='beer_detail'),

    # beers/add/
    url(r'^beers/add/$', AddBeerView.as_view(), name='add_beer'),


    url(r'^breweries/add/$', AddBreweryView.as_view(), name='add_brewery'),

    # breweries/123/
    url(r'^breweries/(?P<pk>[0-9]+)/$', BreweryDetailView.as_view(), name='brewery_detail'),

    # user/
    url(r'^user/(?P<pk>[0-9]+)/$', UserDetailView.as_view(), name='user_detail'),

    # /signup/
    url(r'^signup/$', SignupView.as_view(), name='signup'),

    # /login
    url(r'^login/$', auth_views.login, name='login'),

    # /logout
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),


]
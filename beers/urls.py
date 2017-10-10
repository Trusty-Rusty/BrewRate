from django.conf.urls import url
from .import views
from .import views as beers_views

app_name = 'beers'

urlpatterns = [
    # /
    url(r'^$', views.MainPage.as_view(), name='main'),

    # /breweries/
    url(r'^breweries$', views.AllBreweries.as_view(), name='breweries'),

    # /beers/
    url(r'^beers$', views.AllBeers.as_view(), name='beers'),

    # beers/123/
    url(r'^beers/(?P<pk>[0-9]+)/$', views.BeerDetailView.as_view(), name='beer_detail'),

    # beers/123/
    url(r'^breweries/(?P<pk>[0-9]+)/$', views.BreweryDetailPage.as_view(), name='brewery_detail'),

    # /beers/signup/
    # url(r'^signup/$', views.signup, name='signup'),     # error - "beers_views.signup"?


]
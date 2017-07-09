from django.conf.urls import url
from .import views

urlpatterns = [
    # /beers/
    url(r'^$', views.index, name='index'),

    # /beers/123/
    url(r'^(?P<beer_id>[0-9]+)/$', views.detail, name='detail'),

    # /breweries/
    url(r'^breweries$', views.breweries, name='breweries')
]
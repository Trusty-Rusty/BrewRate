from django.conf.urls import url
from .import views

app_name = 'beers'

urlpatterns = [
    # /beers/
    url(r'^$', views.index, name='index'),

    # /beers/123/
    url(r'^(?P<brewery_id>[0-9]+)/$', views.detail, name='detail'),

    # /breweries/
    url(r'^breweries$', views.breweries, name='breweries')
]
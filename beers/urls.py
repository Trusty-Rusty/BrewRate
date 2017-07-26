from django.conf.urls import url
from .import views
from .import views as beers_views

app_name = 'beers'

urlpatterns = [
    # /beers/signup/
    url(r'^signup/$', views.signup, name='signup'),     # error - "beers_views.signup"?

    # /
    url(r'^$', views.index, name='index'),

    # /123/
    url(r'^(?P<beer_id>[0-9]+)/$', views.detail, name='detail'),

    # /breweries/
    url(r'^breweries$', views.breweries, name='breweries')
]
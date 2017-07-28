from django.conf.urls import url
from .import views
from .import views as beers_views

app_name = 'beers'

urlpatterns = [
    # /
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /beers/signup/
    url(r'^signup/$', views.signup, name='signup'),     # error - "beers_views.signup"?

    # /123/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # /breweries/
    # url(r'^breweries$', views.breweries, name='breweries')
]
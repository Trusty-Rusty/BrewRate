from django.conf.urls import url
from .import views

app_name = 'beers'

urlpatterns = [
    # /beers/
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'register/$', views.UserFormView.as_view(), name='register'),

    # /beers/<brewery_id>/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # /breweries/
    url(r'^breweries$', views.IndexView.as_view(), name='breweries'),

    # /beers/brewery/add/
    url(r'^brewery/add/$', views.BreweryCreate.as_view(), name='brewery-add'),

    # /beers/brewery/2/
    url(r'brewery/(?P<pk>[0-9]+)/$', views.BreweryUpdate.as_view(), name='brewery-update'),

    # /beers/brewery/2/update/
    url(r'brewery/(?P<pk>[0-9]+)/delete/$', views.BreweryDelete.as_view(), name='brewery-delete'),

]
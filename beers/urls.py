from django.conf.urls import url
from .import views


app_name = 'beers'

urlpatterns = [
    # /beers/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /beers/123/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
]
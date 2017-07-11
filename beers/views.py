from django.views import generic
from .models import Beer, Brewery


class IndexView(generic.ListView):
    template_name = 'beers/index.html'
    context_object_name = 'all_breweries'

    def get_queryset(self):
        return Brewery.objects.all()


class DetailView(generic.DetailView):
    model = Brewery
    template_name = 'beers/detail.html'

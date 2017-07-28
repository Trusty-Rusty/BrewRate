from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from .models import Brewery, Beer, Style

# Generic views
class IndexView(generic.ListView):
    template_name = 'beers/index.html'

    def get_queryset(self):
        return Beer.objects.all()


class DetailView(generic.DetailView):
        model = Beer
        template_name = 'beers/detail.html'



# -----------------------------------------------------------------------------------
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
    return render(request, 'beers/signup.html', {'form': form})


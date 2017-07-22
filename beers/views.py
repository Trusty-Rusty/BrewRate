from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View
from .models import Brewery
from .forms import UserForm


class IndexView(generic.ListView):
    template_name = 'beers/index.html'

    def get_queryset(self):
        return Brewery.objects.all()


class DetailView(generic.DetailView):
    model = Brewery
    template_name = 'beers/detail.html'


class BreweryCreate(CreateView):
    model = Brewery
    fields = ['brewery_name', 'brewery_location', 'brewery_founding', 'brewery_logo']


class BreweryUpdate(UpdateView):
    model = Brewery
    fields = ['brewery_name', 'brewery_location', 'brewery_founding', 'brewery_logo']


class BreweryDelete(DeleteView):
    model = Brewery
    success_url = reverse_lazy('beers:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'beers/registration_form.html'

    # blank user form is rendered
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # when user form is filled out and submitted
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # sanitized user data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if credentials are valid
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('beers:index')

        return render(request, self.template_name, {'form': form})
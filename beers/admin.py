from django.contrib import admin
from .models import Brewery, Beer, Rating, Style

# Register your models here.
admin.site.register(Brewery)
admin.site.register(Beer)
admin.site.register(Rating)
admin.site.register(Style)

from django.contrib import admin
from .models import Brewery, Beer

# Register your models here.
admin.site.register(Brewery)
admin.site.register(Beer)

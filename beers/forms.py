from django import forms
from .models import Rating, Brewery, User

'''
class BreweryForm(forms.ModelForm):
    class Meta:
        model = Brewery
        fields = ('brewery_name', 'brewery_location', 'brewery_founding', 'brewery_logo', 'brewery_photo')



class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)
'''

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('rating_score',)





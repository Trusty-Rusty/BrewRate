from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User


# Added breweries that can be assigned to beers as they are added.
class Brewery(models.Model):
    brewery_add_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    brewery_name = models.CharField(max_length=100)
    brewery_location = models.CharField(max_length=250)
    brewery_founding = models.PositiveSmallIntegerField()                # year of founding
    brewery_logo = models.URLField(max_length=100)
    brewery_photo = models.FileField(blank=True)                         # photo of establishment

    def __str__(self):
        return self.brewery_name

# beer styles to be assigned to new beers.  Possibly searchable.
class Style(models.Model):
    STYLE_GROUP = (('ALE', 'Ale'), ('LGR', 'Lager'))                    # all beers must be ale or lager for now

    style_name = models.CharField(max_length=100)
    style_group = models.CharField(max_length=3, choices=STYLE_GROUP)   # ale or lager
    style_country = models.CharField(max_length=100)                    # country of origin

    def __str__(self):
        return self.style_name


# Beer class will store all beers that are submitted by users and link them to styles and breweries
class Beer(models.Model):
    beer_add_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    beer_name = models.CharField(max_length=100)
    beer_brewery = models.ForeignKey(Brewery, on_delete=models.PROTECT)  # reference to brewery
    beer_style = models.ForeignKey(Style, on_delete=models.PROTECT)  # reference to style
    beer_abv = models.DecimalField(null=True, max_digits=3, decimal_places=1)      # abv in x.x or xx.x format
    beer_srm = models.PositiveSmallIntegerField(null=True, validators=[MaxValueValidator(99)])     # beer color in SRM
    beer_logo = models.URLField(max_length=100)
    beer_photo = models.FileField(blank=True)                                     # photo of beer while drinking it

    def __str__(self):
        return self.beer_name


# user ratings for each beer-user pair.  Join table with many-to-many relationship
class Rating(models.Model):

    # variables to represent possible ratings for extensibility and maintainability
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'

    # Rating choices
    RATINGS = (
        (ONE, '*'), (TWO, '**'),
        (THREE, '***'), (FOUR, '****'),
        (FIVE, '*****'))

    rating_user = models.ForeignKey(User, on_delete=models.PROTECT)     # ref to user id
    rating_beer = models.ForeignKey(Beer, on_delete=models.PROTECT)     # ref to beer id
    rating_score =models.CharField(null=True, max_length=5, choices=RATINGS)       #unique rating for user and beer

    def __str__(self):
        return str(self.rating_user) + ' rated ' + str(self.rating_beer) + ' - ' + str(self.rating_score)

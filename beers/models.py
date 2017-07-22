from django.db import models
from django.core.urlresolvers import reverse


# Brewery class will store all breweries submitted by users when adding beers.
# As they are added they will populate a dropdown in the future

class Brewery(models.Model):
    brewery_name = models.CharField(max_length=100)
    brewery_location = models.CharField(max_length=250)
    brewery_founding = models.IntegerField()
    brewery_logo = models.FileField()

    # forward to detail page when new album is created
    def get_absolute_url(self):
        return reverse('beers:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.brewery_name + ' - ' + self.brewery_location

#
# Beer class will store all beers that are submitted byt users

class Beer(models.Model):
    BEER_STYLES = (
        ('ASA', 'American Strong Ale'), ('AMW', 'American Wheat'), ('BAW', 'Barleywine'), ('BNA', 'Brown Ale'),
        ('CAC', 'California Common'), ('ESB', 'Extra Special Bitter'), ('HEF', 'Hefeweizen'),
        ('IPA', 'India Pale Ale'), ('OKT', 'Oktoberfest'), ('PAL', 'Pale Ale'), ('PIL', 'Pilsner'),
        ('PTR', 'Porter'), ('QUD', 'Quadrupel'), ('STT', 'Stout'), ('VNL', 'Vienna Lager')
    )

    beer_name = models.CharField(max_length=100)
    beer_brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)  # all beers by certain brewery deleted w/ brewery
    beer_style = models.CharField(max_length=3, choices=BEER_STYLES)  # possible styles are chosen from list
    beer_logo = models.URLField(max_length=100)
    beer_fav = models.BooleanField(default=False)

    def __str__(self):
        return self.beer_name + ' - ' + str(self.beer_brewery)



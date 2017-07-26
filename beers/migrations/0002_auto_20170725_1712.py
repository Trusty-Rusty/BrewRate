# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 17:12
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('beers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style_name', models.CharField(max_length=100)),
                ('style_group', models.CharField(choices=[(b'ALE', b'Ale'), (b'LGR', b'Lager')], max_length=3)),
                ('style_country', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='beer',
            name='beer_abv',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
        migrations.AddField(
            model_name='beer',
            name='beer_photo',
            field=models.FileField(blank=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='beer',
            name='beer_srm',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(99)]),
        ),
        migrations.AddField(
            model_name='brewery',
            name='brewery_photo',
            field=models.FileField(blank=True, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='beer',
            name='beer_brewery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='beers.Brewery'),
        ),
        migrations.AlterField(
            model_name='beer',
            name='beer_style',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='beers.Style'),
        ),
        migrations.AddField(
            model_name='rating',
            name='rating_beer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='beers.Beer'),
        ),
        migrations.AddField(
            model_name='rating',
            name='rating_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]

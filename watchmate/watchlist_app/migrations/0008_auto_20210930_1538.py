# Generated by Django 3.2.7 on 2021-09-30 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0007_alter_review_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='number_rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='rating_avg',
            field=models.FloatField(default=0),
        ),
    ]

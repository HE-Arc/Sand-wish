# Generated by Django 2.1.7 on 2019-02-22 16:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sandwish_app', '0002_auto_20190221_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, unique=True),
            preserve_default=False,
        ),
    ]

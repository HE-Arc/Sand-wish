# Generated by Django 2.1.7 on 2019-02-28 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sandwish_app', '0004_remove_wishlist_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gift',
            old_name='user',
            new_name='wishlist',
        ),
    ]

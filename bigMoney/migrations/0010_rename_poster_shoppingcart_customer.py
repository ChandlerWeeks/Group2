# Generated by Django 4.2 on 2023-04-06 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bigMoney', '0009_alter_merchandise_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppingcart',
            old_name='poster',
            new_name='customer',
        ),
    ]

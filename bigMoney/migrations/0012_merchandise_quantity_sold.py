# Generated by Django 4.2 on 2023-04-06 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bigMoney', '0011_alter_merchandise_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchandise',
            name='quantity_sold',
            field=models.IntegerField(default=0),
        ),
    ]

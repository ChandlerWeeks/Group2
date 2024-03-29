# Generated by Django 4.1.7 on 2023-03-28 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bigMoney', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='New User', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='', max_length=255),
        ),
    ]

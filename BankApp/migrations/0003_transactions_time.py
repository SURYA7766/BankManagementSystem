# Generated by Django 3.1.7 on 2021-03-24 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BankApp', '0002_auto_20210324_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='Time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
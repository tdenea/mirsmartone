# Generated by Django 3.2.13 on 2022-06-10 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_textualpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formcontact',
            name='country',
        ),
        migrations.RemoveField(
            model_name='formcontact',
            name='page',
        ),
        migrations.RemoveField(
            model_name='formcontact',
            name='product',
        ),
    ]
# Generated by Django 3.2.13 on 2022-08-04 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20220613_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lang',
            field=models.CharField(choices=[('en', 'English'), ('it', 'Italian'), ('de', 'German'), ('fr', 'French'), ('es', 'Spanish')], default='en', max_length=10, verbose_name='Preferred language'),
        ),
    ]

# Generated by Django 3.2.13 on 2022-06-10 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20220610_1023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formcontact',
            name='surname',
        ),
        migrations.AlterField(
            model_name='formcontact',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Fullname'),
        ),
    ]
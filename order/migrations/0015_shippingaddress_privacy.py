# Generated by Django 3.2.13 on 2022-07-14 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_auto_20220704_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='privacy',
            field=models.BooleanField(default=False, verbose_name='I have read the privacy policy at this link'),
        ),
    ]

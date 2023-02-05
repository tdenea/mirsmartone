# Generated by Django 3.2.13 on 2022-08-02 07:40

from django.db import migrations
import oscar.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0022_auto_20210210_0539'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='gtin',
            field=oscar.models.fields.NullCharField(max_length=64, unique=True, verbose_name='Codice GTIN'),
        ),
    ]
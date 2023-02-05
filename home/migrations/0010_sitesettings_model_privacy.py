# Generated by Django 3.2.13 on 2022-07-07 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0012_uploadeddocument'),
        ('home', '0009_sitesettings_google_analytics_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='model_privacy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.document', verbose_name='Modello esercizio diritti in materia di protezione dei dati personali'),
        ),
    ]
# Generated by Django 3.2.13 on 2022-06-01 14:23

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('home', '0003_auto_20220513_1059'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextualPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('title_it', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('title_de', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('title_fr', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('title_es', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('description', wagtail.core.fields.RichTextField(blank=True, null=True, verbose_name='Description')),
                ('description_it', wagtail.core.fields.RichTextField(blank=True, null=True, verbose_name='Description')),
                ('description_de', wagtail.core.fields.RichTextField(blank=True, null=True, verbose_name='Description')),
                ('description_fr', wagtail.core.fields.RichTextField(blank=True, null=True, verbose_name='Description')),
                ('description_es', wagtail.core.fields.RichTextField(blank=True, null=True, verbose_name='Description')),
                ('slug_it', models.SlugField(max_length=255)),
                ('slug_de', models.SlugField(max_length=255)),
                ('slug_fr', models.SlugField(max_length=255)),
                ('slug_es', models.SlugField(max_length=255)),
                ('seo_title_it', models.CharField(blank=True, max_length=255, null=True, verbose_name='Title tag it')),
                ('seo_title_de', models.CharField(blank=True, max_length=255, null=True, verbose_name='Title tag de')),
                ('seo_title_fr', models.CharField(blank=True, max_length=255, null=True, verbose_name='Title tag fr')),
                ('seo_title_es', models.CharField(blank=True, max_length=255, null=True, verbose_name='Title tag es')),
                ('search_description_it', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta description it')),
                ('search_description_de', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta description de')),
                ('search_description_fr', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta description fr')),
                ('search_description_es', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta description es')),
            ],
            options={
                'verbose_name': 'Textual Page',
            },
            bases=('wagtailcore.page',),
        ),
    ]

from oscar.apps.dashboard.catalogue import forms as base_forms
from django import forms
from catalogue.models import Product

class ProductForm(base_forms.ProductForm):
    class Meta(base_forms.ProductForm.Meta):
        model = Product
        fields = ('title', 'title_en' ,'upc', 'gtin', 'description', 'is_public', 'is_discountable', 'structure', 'slug', 'meta_title',
            'meta_description')
        widgets = {
            'structure': forms.HiddenInput(),
            'meta_description': forms.Textarea(attrs={'class': 'no-widget-init'})
        }
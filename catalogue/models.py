from oscar.apps.catalogue.abstract_models import AbstractProduct
from oscar.models.fields import NullCharField
from django.utils.translation import gettext_lazy as _

class Product(AbstractProduct):
    title = NullCharField('Titolo', max_length=200, blank=True, null=True,)
    title_en = NullCharField('Titolo EN' , max_length=200, blank=True, null=True)
    gtin = NullCharField('Codice GTIN', max_length=64, blank=True, null=True, unique=True,)

from oscar.apps.catalogue.models import * # noqa isort:skip

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from oscar.apps.address.abstract_models import AbstractBillingAddress, AbstractUserAddress
from django.utils.translation import gettext_lazy as _

class UserAddress(AbstractUserAddress):
    requested_invoice = models.BooleanField(default=False)
    cf = models.CharField(max_length=16, blank=True, null=True, verbose_name=_('Codice Fiscale'))
    piva = models.CharField(max_length=16, blank=True, null=True, verbose_name=_('Partita Iva'))
    phone_number = PhoneNumberField(
        _("Phone number"), blank=True,
        help_text=_("In case we need to call you about your order"))

    #base_fields = ['salutation', 'line1', 'line2', 'line3', 'line4', 'state', 'postcode', 'country','cf_piva','requested_invoice']
    base_fields = ['salutation', 'line1', 'line2', 'line3', 'line4', 'state', 'postcode', 'country','cf','piva','requested_invoice']
    hash_fields = ['salutation', 'line1', 'line2', 'line3', 'line4', 'state', 'postcode', 'country']
    base_shipping_fields = ['salutation', 'line1', 'line2', 'line3', 'line4', 'state', 'postcode', 'country','phone_number']
    def get_field_values(self, fields):
        field_values = []
        for field in fields:
            # Title is special case
            if field == 'title':
                value = self.get_title_display()
            elif field == 'country':
                try:
                    value = self.country.printable_name
                except exceptions.ObjectDoesNotExist:
                    value = ''
            elif field == 'salutation':
                value = self.salutation
            elif field == 'requested_invoice':
                value = 'Invoice requested' if self.requested_invoice else 'Invoice not requested'
            elif field == 'phone_number':
                value = str(self.phone_number)
            else:
                value = getattr(self, field)
            field_values.append(value)
        return field_values
    
    def active_shipping_address_fields(self):
        return self.get_address_field_values(self.base_shipping_fields)

from oscar.apps.address.models import *  # noqa isort:skip

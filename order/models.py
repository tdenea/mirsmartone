from oscar.apps.address.abstract_models import AbstractBillingAddress,AbstractShippingAddress
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import exceptions

class BillingAddress(AbstractBillingAddress):
    requested_invoice = models.BooleanField(default=False)
    cf = models.CharField(max_length=16, blank=True, null=True, verbose_name=_('Codice Fiscale'))
    piva = models.CharField(max_length=16, blank=True, null=True, verbose_name=_('Partita Iva'))
    
    phone_number = models.CharField(_("Phone number"), max_length=16,  blank=True, null=True)
    notes = models.TextField(
        blank = True,
        null = True,
        verbose_name=_('Instructions'),
        help_text=_("Tell us anything we should know when delivering "
                    "your order."),
        default = '-'
        )
    terms_and_conditions_expressly = models.BooleanField(default=False, verbose_name=_('Pursuant to and for the purposes of Articles 1341 and 1342 of the Italian Civil Code, the Professional Customer declares that he/she expressly and unconditionally accepts Articles 5 (transport and delivery), 8 (Errors and limitations of liability) and 10 (Applicable law and competent court).'))

    base_fields = ['salutation', 'line1', 'line2', 'line3', 'line4', 'state', 'postcode', 'country','cf','piva','requested_invoice', 'terms_and_conditions_expressly']

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
            elif field == 'terms_and_conditions_expressly':
                value = ''
                # value = 'Terms and conditions accepted' if self.terms_and_conditions_expressly else 'Terms and conditions not accepted'
            else:
                value = getattr(self, field)
            field_values.append(value)
        return field_values

class ShippingAddress(AbstractShippingAddress):
    privacy = models.BooleanField(default=False, verbose_name=_('I have read the privacy policy at this link'))
    terms_and_conditions = models.BooleanField(default=False, verbose_name=_('I accept General Terms and Conditions of Sale'))

    base_fields  = ['salutation', 'line1', 'line2', 'line3', 'line4', 'state', 'postcode', 'country','phone_number', 'privacy','terms_and_conditions']

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
            # elif field == 'requested_invoice':
            #     value = 'Invoice requested' if self.requested_invoice else 'Invoice not requested'
            elif field == 'terms_and_conditions':
                value = ''
                # value = 'Terms and conditions accepted' if self.terms_and_conditions else 'Terms and conditions not accepted'
            elif field == 'privacy':
                value = ''
            elif field == 'phone_number':
                value = str(self.phone_number)
            else:
                value = getattr(self, field)
            field_values.append(value)
        return field_values

from oscar.apps.order.models import *  # noqa isort:skip

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from oscar.core.loading import get_model
from oscar.apps.checkout.forms import ShippingAddressForm as CoreShippingAddressForm
from oscar.apps.payment.forms import BillingAddressForm as CoreBillingAddressForm
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from order.models import BillingAddress
from checkout.validators import validate_codice_fiscale, validate_partita_iva

UserAddress = get_model('address', 'UserAddress')
Country = get_model('address', 'Country')

class BillingAddressForm(CoreBillingAddressForm):
    first_name = forms.CharField(
        label=_('Nome / Nome referente'),
    )
    last_name = forms.CharField(
        label=_('Cognome / Ragione Sociale'),
    )
    line1 = forms.CharField(
        label=_('Indirizzo'),
    )
    line4 = forms.CharField(
        label=_('Città'),
        help_text=_("Se non trovi la tua città, contattaci")
    )
    state = forms.CharField(
        label=_('Provincia'),
    )
    postcode = forms.CharField(
        label=_('CAP'),
    )
    # https://github.com/stefanfoulis/django-phonenumber-field/issues/202
    phone_number = forms.CharField(
        label=_('Phonenumber'),
        widget=forms.HiddenInput(),
        required=False
    )

    notes = forms.CharField(
        widget=forms.HiddenInput(),
        label=_('Note'),
        required=False,
    )

    requested_invoice = forms.BooleanField(
        label=_('I would like an invoice'),
        required=False
    )

    cf = forms.CharField(
        label=_('Codice Fiscale'),
        required=False
    )

    piva = forms.CharField(
        label=_('Partita IVA'),
        required=False
    )

    class Meta:
        model = BillingAddress
        fields = [
            'requested_invoice',
            'first_name', 'last_name',
            'country', 'state', 'line4',
            'line1', 
            'postcode', 
            'cf', 'piva', 'phone_number', 'terms_and_conditions_expressly'
        ]
        help_texts = {
            'line4': _("Se non trovi la tua città, contattaci"),
        }
    
    # def __init__(self, *args, **kwargs):
    #     super(BillingAddressForm, self).__init__(*args, **kwargs)
    #     self.fields['terms_and_conditions_expressly'].required = True

    def set_country_queryset(self):
        self.fields['country'].queryset = Country.objects.filter(
            is_shipping_country=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adjust_country_field()

    def adjust_country_field(self):
        countries = Country._default_manager.filter(
            is_shipping_country=True)

        # No need to show country dropdown if there is only one option
        if len(countries) == 1:
            self.fields.pop('country', None)
            self.instance.country = countries[0]
        else:
            self.fields['country'].queryset = countries
            self.fields['country'].empty_label = None

    # def clean(self):
    #     cleaned_data = super().clean()
    #     cf = cleaned_data['cf']
    #     piva = cleaned_data['piva']

    #     if cleaned_data['requested_invoice']:
    #         cf = cf.upper()
    #         piva = piva.upper()
    #         if not cf:
    #             raise ValidationError(
    #                 _('Inserisci un codice fiscale se vuoi la fattura'))

    #         # cf e piva presenti entrambi e uguali devono essere una partita iva valida
    #         if cf and piva and cf == piva:
    #             if not validate_partita_iva(cf):
    #                 raise ValidationError(
    #                     _('Inserisci un codice fiscale formalmente valido'))
    #             if not validate_partita_iva(piva):
    #                 raise ValidationError(
    #                     _('Inserisci una partita IVA formalmente valida'))
    #             cleaned_data['cf'] = cf
    #             cleaned_data['piva'] = piva
    #             return cleaned_data

    #         # cf e piva presenti entrambi
    #         if cf and piva and cf != piva:
    #             # caso in cui il cf non e' personale ma aziendale di 11 cifre
    #             if not validate_codice_fiscale(cf) and len(cf) != 11:
    #                 raise ValidationError(
    #                     _('Inserisci un codice fiscale aziendale valido di 11 cifre o un codice fiscale personale valido'))

    #             # caso in cui il codice fiscale e' personale o aziendale valido va controllata solo la piva
    #             if not validate_partita_iva(piva):
    #                 raise ValidationError(
    #                     _('Inserisci una partita IVA formalmente valida'))
    #             cleaned_data['cf'] = cf
    #             cleaned_data['piva'] = piva
    #             return cleaned_data

    #         # caso in cui c'e' solo il codice fiscale personale
    #         if not piva and not validate_codice_fiscale(cf):
    #             raise ValidationError(
    #                 _('Inserisci un codice fiscale formalmente valido'))

    #         cleaned_data['cf'] = cf
    #     return cleaned_data


class ShippingAddressForm(CoreShippingAddressForm):

    first_name = forms.CharField(
        label=_('Nome'),
    )
    last_name = forms.CharField(
        label=_('Cognome'),
    )
    line1 = forms.CharField(
        label=_('Indirizzo'),
    )
    line4 = forms.CharField(
        label=_('Città'),
        help_text=_("Se non trovi la tua città, contattaci")
    )
    state = forms.CharField(
        label=_('Provincia'),
    )
    postcode = forms.CharField(
        label=_('CAP'),
    )
    phone_number = PhoneNumberField(label=_('Numero di Telefono'))

    notes = forms.CharField(
        label=_('Note'),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(ShippingAddressForm, self).__init__(*args, **kwargs)
        self.fields['privacy'].required = True
        self.fields['terms_and_conditions'].required = True

    class Meta:
        model = get_model('order', 'ShippingAddress')

        fields = [
            'first_name', 'last_name',
            'country', 'state', 'line4',
            'line1', 
            'postcode', 
            'phone_number', 'notes', 'privacy','terms_and_conditions',
        ]
        help_texts = {
            'line4': _("Se non trovi la tua città, contattaci"),
        }


class PaymentMethodForm(forms.Form):
    """
    Extra form for the custom payment method.
    """

    payment_method = forms.ChoiceField(
        label=_("Select a payment method"),
        choices=settings.OSCAR_PAYMENT_METHODS,
        widget=forms.RadioSelect(),
    )

def get_payment_method_display(payment_method):
    return dict(settings.OSCAR_PAYMENT_METHODS).get(payment_method)

from oscar.apps.address.forms import UserAddressForm as CoreUserAddressForm
from oscar.core.loading import get_model
from django.utils.translation import gettext_lazy as _
from django import forms

Country = get_model('address', 'Country')
UserAddress = get_model('address', 'useraddress')


class UserAddressForm(CoreUserAddressForm):
    class Meta:
        model = UserAddress
        fields = [
            'first_name', 'last_name',
            'country', 'state', 'line4',
            'line1', 'line2', 'line3',
            'postcode',
            'phone_number', 'notes',
        ]
        help_texts = {
            'line4': _("Se non trovi la tua città, contattaci"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        countries = Country._default_manager.filter(
            is_shipping_country=True)
        self.fields['country'].queryset = countries


class ShippingUserAddressForm(UserAddressForm):
    cf = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )
    piva = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )

    class Meta:
        model = UserAddress
        fields = [
            'first_name', 'last_name',
            'country', 'state', 'line4',
            'line1',
            'postcode',
            'phone_number', 'notes'
        ]
        help_texts = {
            'line4': _("Se non trovi la tua città, contattaci"),
        }

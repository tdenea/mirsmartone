from oscar.apps.checkout.session import CheckoutSessionMixin as CoreCheckoutSessionMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from oscar.apps.checkout import exceptions

class CheckoutSessionMixin(CoreCheckoutSessionMixin):
    pass
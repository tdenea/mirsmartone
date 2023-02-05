import oscar.apps.checkout.apps as apps
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from oscar.core.application import OscarConfig
from oscar.core.loading import get_class


class CheckoutConfig(apps.CheckoutConfig):
    label = "checkout"
    name = "checkout"
    verbose_name = _("Checkout")

    namespace = "checkout"

    def ready(self):
        self.index_view = get_class("checkout.views", "IndexView")
        self.shipping_address_view = get_class(
            "checkout.views", "ShippingAddressView")
        self.user_address_update_view = get_class(
            "checkout.views", "UserAddressUpdateView"
        )
        self.user_billing_address_update_view = get_class('checkout.views',
                                                          'UserBillingAddressUpdateView')
        self.user_address_delete_view = get_class(
            "checkout.views", "UserAddressDeleteView"
        )
        self.shipping_method_view = get_class(
            "checkout.views", "ShippingMethodView")
        self.billing_address_view = get_class(
            'checkout.views', 'BillingAddressView')
        self.payment_method_view = get_class(
            "checkout.views", "PaymentMethodView")
        self.payment_details_view = get_class(
            "checkout.views", "PaymentDetailsView")
        self.thankyou_view = get_class("checkout.views", "ThankYouView")

        self.freeze_basket_view = get_class(
            "checkout.views", "FreezeBasketView")
        self.thaw_basket_view = get_class("checkout.views", "ThawBasketView")
        self.paypal_error_view = get_class("checkout.views", "PaypalErrorView")
        self.place_order_view = get_class("checkout.views", "PlaceOrderView")

    def get_urls(self):
        urls = [
            url(r"^$", self.index_view.as_view(), name="index"),
            # Shipping/user address views
            url(
                r"shipping-address/$",
                self.shipping_address_view.as_view(),
                name="shipping-address",
            ),
            url(r'billing-address/$',
                self.billing_address_view.as_view(), name='billing-address'),
            url(
                r"user-address/edit/(?P<pk>\d+)/$",
                self.user_address_update_view.as_view(),
                name="user-address-update",
            ),
            url(r'user-billing-address/edit/(?P<pk>\d+)/$',
                self.user_billing_address_update_view.as_view(),
                name='user-billing-address-update'),
            url(
                r"user-address/delete/(?P<pk>\d+)/$",
                self.user_address_delete_view.as_view(),
                name="user-address-delete",
            ),
            # Shipping method views
            url(
                r"shipping-method/$",
                self.shipping_method_view.as_view(),
                name="shipping-method",
            ),
            # Payment views
            url(
                r"payment-method/$",
                self.payment_method_view.as_view(),
                name="payment-method",
            ),
            url(
                r"payment-details/$",
                self.payment_details_view.as_view(),
                name="payment-details",
            ),
            # utils
            url(
                r"freeze-basket/$",
                self.freeze_basket_view.as_view(),
                name="freeze_basket",
            ),
            url(
                r"thaw-basket/$",
                self.thaw_basket_view.as_view(),
                name="thaw_basket",

            ),
            url(
                r"paypal-error/$",
                self.paypal_error_view.as_view(),
                name="paypal_error",
            ),
            # Preview and thankyou
            url(
                r"preview/$",
                self.payment_details_view.as_view(preview=True),
                name="preview",
            ),
            url(
                r"place-order/$",
                self.place_order_view.as_view(preview=True),
                name="place-order",
            ),
            url(r"thank-you/$", self.thankyou_view.as_view(), name="thank-you"),
        ]
        return self.post_process_urls(urls)

    def get_url_decorator(self, pattern):
        if not settings.OSCAR_ALLOW_ANON_CHECKOUT:
            return login_required
        if pattern.name.startswith("user-address"):
            return login_required
        return None

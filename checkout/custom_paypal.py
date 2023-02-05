import logging
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from oscar.core.loading import get_class, get_model
from home.views import send_email_to_admin
from paypal.express.views import SuccessResponseView as CoreSuccessResponseView
from paypal.express.views import RedirectView as OscarPaypalRedirectView

from pprint import pprint

logger = logging.getLogger('paypal.express')

Applicator = get_class('offer.applicator', 'Applicator')
Basket = get_model('basket', 'Basket')
Selector = get_class('partner.strategy', 'Selector')
ShippingAddress = get_model('order', 'ShippingAddress')
Country = get_model('address', 'Country')

class SuccessResponseView(CoreSuccessResponseView):
    def get(self, request, *args, **kwargs):
        """
        Fetch details about the successful transaction from PayPal.  We use
        these details to show a preview of the order with a 'submit' button to
        place it.
        """
        
        super(SuccessResponseView, self).get(request, *args, **kwargs)
        print(SuccessResponseView)
        basket = Basket.objects.get(id=kwargs['basket_id'])
        if Selector:
            basket.strategy = Selector().strategy(request)
        
        # Re-apply any offers
        Applicator().apply(basket, request.user, request=request)
        
        if not basket:
            messages.error(self.request, _("No basket was found that corresponds to your "
                                        "PayPal transaction"))
            return HttpResponseRedirect(reverse('basket:summary'))  
        
        submission = self.build_submission(basket=basket)
        self.submit(**submission)
        order = basket.order_set.first()
        # Correzione user
        print("correzione user")
        print(order)
        print(order.basket.owner)
        print(basket.owner)
        order.user = order.basket.owner
        order.guest_email = ''
        order.save()
        # Invio della mail verso admin
        send_email_to_admin(obj=order, typology="order")
        return HttpResponseRedirect(reverse('checkout:thank-you'))

    def get_shipping_address(self, basket):
        """
        Return a created shipping address instance, created using
        the data returned by PayPal.
        """
        # Determine names - PayPal uses a single field
        # nla - To pull over the phone number/notes from the entered address
        #old_shipping = super( SuccessResponseView, self).get_shipping_address( basket )
        ship_to_name = self.txn.value('PAYMENTREQUEST_0_SHIPTONAME')
        if ship_to_name is None:
            return None
        first_name = last_name = ''
        parts = ship_to_name.split()
        if len(parts) == 1:
            last_name = ship_to_name
        elif len(parts) > 1:
            first_name = parts[0]
            last_name = " ".join(parts[1:])
        phone_number=self.txn.value('PAYMENTREQUEST_0_SHIPTOPHONENUM', default="")
        
        return ShippingAddress(
            first_name=first_name,
            last_name=last_name,
            line1=self.txn.value('PAYMENTREQUEST_0_SHIPTOSTREET'),
            line2=self.txn.value('PAYMENTREQUEST_0_SHIPTOSTREET2', default=""),
            line4=self.txn.value('PAYMENTREQUEST_0_SHIPTOCITY', default=""),
            state=self.txn.value('PAYMENTREQUEST_0_SHIPTOSTATE', default=""),
            postcode=self.txn.value('PAYMENTREQUEST_0_SHIPTOZIP', default=""),
            country=Country.objects.get(iso_3166_1_a2=self.txn.value('PAYMENTREQUEST_0_SHIPTOCOUNTRYCODE')),
            # nla - Move over notes and phone numbers that don't come thru PP
            phone_number=self.txn.value('PAYMENTREQUEST_0_SHIPTOPHONENUM', default=""),
        )

class RedirectView(OscarPaypalRedirectView):
    as_payment_method = True

    def get_redirect_url(self, **kwargs):
        url = super().get_redirect_url(**kwargs)
        if url == reverse('checkout:payment-details'):
            url = reverse('checkout:payment-method')
        return url
        
    def _get_paypal_params(self):
        print('_get_paypal_params')
        basket = self.request.basket
        params ={}
        params['SHIPTOPHONENUM'] = self.get_shipping_address(basket).phone_number
        print('PARAMS')
        pprint(params)
        return params
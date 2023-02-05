import json
from decimal import Decimal
import logging
from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest
from oscar.core.loading import get_model, get_class
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from address.forms import UserAddressForm, ShippingUserAddressForm
from checkout.forms import ShippingAddressForm, BillingAddressForm
from oscar.apps.checkout.views import ShippingAddressView as CoreShippingAddressView
from oscar.apps.checkout.views import ShippingMethodView as CoreShippingMethodView
from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
from oscar.apps.checkout.views import PaymentMethodView as CorePaymentMethodView
from oscar.apps.checkout.views import UserAddressUpdateView as CoreUserAddressUpdateView
from oscar.apps.checkout.views import ThankYouView as CoreThankYouView
from django.views.generic import FormView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponse
from oscar.apps.checkout.calculators import OrderTotalCalculator
from home.views import send_email_to_admin

from . import forms

Country = get_model("address", "Country")
SourceType = get_model("payment", "SourceType")
Source = get_model("payment", "Source")
Selector = get_class("partner.strategy", "Selector")
Basket = get_model("basket", "Basket")
UserAddress = get_model('address', 'UserAddress')
CheckoutSessionData = get_class('checkout.utils', 'CheckoutSessionData')
CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')
ShippingAddress = get_model('order', 'ShippingAddress')
BillingAddress = get_model('order', 'BillingAddress')
OrderNumberGenerator = get_class('order.utils', 'OrderNumberGenerator')
Repository = get_class('shipping.repository', 'Repository')
try:
    Applicator = get_class('offer.applicator', 'Applicator')
except ModuleNotFoundError:
    # fallback for django-oscar<=1.1
    Applicator = get_class('offer.utils', 'Applicator')

# LOGGING

# Get an instance of a logger
logger = logging.getLogger('debugging')

class ShippingAddressView(CoreShippingAddressView):

    def get_available_addresses(self):
        # Include only addresses where the country is flagged as valid for
        # shipping. Also, use ordering to ensure the default address comes
        # first.
        return self.request.user.addresses.filter(country__is_shipping_country=True).order_by('-is_default_for_shipping')

class ShippingMethodView(CoreShippingMethodView):
    def get_success_response(self):
        return redirect("checkout:payment-method")

    def get_context_data(self, **kwargs):
        ctx = super(ShippingMethodView, self).get_context_data(**kwargs)
        ctx.update({"payment_method": None})
        ctx.update({"show_tax_separately": False})
        return ctx


class FreezeBasketView(View):
    def get(self, request, *args, **kwargs):
        # print("freeze basket view")
        try:
            self.request.basket.freeze()
            print(self.request.basket.id, self.request.basket.status)
            self.request.session['frozen_basket_id'] = self.request.basket.id
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=400)


class ThawBasketView(View):
    def get(self, request, *args, **kwargs):
        try:
            Basket.objects.filter(
                id=self.request.session['frozen_basket_id']).first().thaw()
            self.request.basket.thaw()
            # print(self.request.basket.id, self.request.basket.status)
            return HttpResponse(status=200)
        except Exception as e:
            print("Exception!", e)
            return HttpResponse(status=400)

class PaypalErrorView(View):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        # print('PAYPAL ERROR/CANCEL', json.loads(body_unicode))
        return HttpResponse(status=200)

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" %
                    type(obj).__name__)


class PaymentDetailsView(CorePaymentDetailsView):
    def handle_payment(self, order_number, total, **kwargs):
        method = self.checkout_session.payment_method()
        # print("payment details view: " + method)

    def get_context_data(self, **kwargs):
        # print("get context paym deta")
        # print(self.checkout_session)
        # print(self.checkout_session.payment_method())
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
        ctx.update({"payment_method": self.checkout_session.payment_method()})
        return ctx


# https://stackoverflow.com/questions/49349883/how-to-add-few-payment-methods-to-django-oscar
class PaymentMethodView(CorePaymentMethodView, FormView):
    """
    View for a user to choose which payment method(s) they want to use.
    This would include setting allocations if payment is to be split
    between multiple sources. It's not the place for entering sensitive details
    like bankcard numbers though - that belongs on the payment details view.
    """

    template_name = "oscar/checkout/payment_method.html"
    step = "payment-method"
    form_class = forms.PaymentMethodForm
    success_url = reverse_lazy("checkout:payment-details")

    def get(self, request, *args, **kwargs):
        if len(settings.OSCAR_PAYMENT_METHODS) == 1:
            self.checkout_session.pay_by(settings.OSCAR_PAYMENT_METHODS[0][0])

            return redirect(self.get_success_url())
        else:
            return FormView.get(self, request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        # print('PAYMENT METHOD: '+ str(self.checkout_session.payment_method()))
        return reverse_lazy("checkout:preview")

    def get_initial(self):
        return {
            "payment_method": self.checkout_session.payment_method(),
        }

    def form_valid(self, form):
        # Store payment method in the CheckoutSessionMixin.checkout_session (a CheckoutSessionData object)
        self.checkout_session.pay_by(form.cleaned_data['payment_method'])
        print(self.checkout_session.payment_method())
        # print('form valid')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(PaymentMethodView, self).get_context_data(**kwargs)
        ctx.update({"payment_method": None})
        ctx.update({"show_tax_separately": True})
        # print('context data')
        print(("paypal", "Paypal") in settings.OSCAR_PAYMENT_METHODS)
        if ("paypal", "Paypal") in settings.OSCAR_PAYMENT_METHODS:
            ctx["paypal_payment"] = True

        if ("cod", "Cash on delivery") in settings.OSCAR_PAYMENT_METHODS:
            ctx["cod_payment"] = True

        return ctx

class ShippingAddressView(CoreShippingAddressView):
    form_class = ShippingAddressForm
    success_url = reverse_lazy('checkout:billing-address')
    def post(self, request, *args, **kwargs):
        # Check if a shipping address was selected directly (e.g. no form was
        # filled in)
       
        if self.request.user.is_authenticated \
                and 'address_id' in self.request.POST:
            address = UserAddress._default_manager.get(
                pk=self.request.POST['address_id'], user=self.request.user)
            action = self.request.POST.get('action', None)
            if action == 'ship_to':
                # User has selected a previous address to ship to
                self.checkout_session.ship_to_user_address(address)
                return redirect(self.get_success_url())
            else:
                return HttpResponseBadRequest()
        else:
            return super().post(
                request, *args, **kwargs)

    def get_default_shipping_address(self):
        if self.request.user.is_authenticated:
            return self.request.user.addresses.filter(is_default_for_shipping=True).first()


    def get_default_shipping_method(self, basket):
        return Repository().get_default_shipping_method(
            basket=self.request.basket, user=self.request.user,
            request=self.request, shipping_addr=self.get_default_shipping_address())


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        method = self.get_default_shipping_method(self.request.basket)
        ctx['shipping_method'] = method
        shipping_charge = method.calculate(self.request.basket)
        ctx['shipping_charge'] = shipping_charge
        if method.is_discounted:
            excl_discount = method.calculate_excl_discount(self.request.basket)
            ctx['shipping_charge_excl_discount'] = excl_discount
        
        ctx['order_total'] = OrderTotalCalculator().calculate(
            self.request.basket, shipping_charge)

        return ctx

class UserBillingAddressUpdateView(CoreUserAddressUpdateView):
    """
    Update a user billing address
    """
    template_name = 'oscar/checkout/user_address_form.html'
    form_class = UserAddressForm
    success_url = reverse_lazy('checkout:billing-address')

class UserAddressUpdateView(CoreUserAddressUpdateView):
    form_class = ShippingUserAddressForm

class ThankYouView(CoreThankYouView):
    def post(self, request, *args, **kwargs):
        # print(self.request.body)
        # print(json.loads(self.request.body))

        return None

class BillingAddressView(CheckoutSessionMixin, generic.FormView):
   
    template_name = 'oscar/checkout/billing_address.html'
    form_class = BillingAddressForm
    success_url = reverse_lazy('checkout:payment-method')
    pre_conditions = ['check_basket_is_not_empty',
                      'check_basket_is_valid',
                      'check_user_email_is_captured']
    skip_conditions = ['skip_unless_basket_requires_shipping']

    def get_initial(self):
        initial = self.checkout_session.new_billing_address_fields()
        if initial:
            initial = initial.copy()
            # Convert the primary key stored in the session into a Country
            # instance
            try:
                initial['country'] = Country.objects.get(
                    iso_3166_1_a2=initial.pop('country_id'))
            except Country.DoesNotExist:
                # Hmm, the previously selected Country no longer exists. We
                # ignore this.
                pass
        return initial

    def get_default_shipping_address(self):
        if self.request.user.is_authenticated:
            return self.request.user.addresses.filter(is_default_for_shipping=True).first()

    def get_default_shipping_method(self, basket):
        # Prendo l'indirizzo scelto dall'utente per far già vedere i prezzi di spedizione
        shipping_address = self.get_shipping_address(basket=self.request.basket)
        return Repository().get_default_shipping_method(
            basket=self.request.basket, user=self.request.user,
            request=self.request, shipping_addr=shipping_address)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Look up address book data
            ctx['addresses'] = self.get_available_addresses()

        #added by me
        method = self.get_default_shipping_method(self.request.basket)

        # Potrebbe generare errori se più di un metodo di spedizione disponibile
        self.checkout_session.use_shipping_method(method.code) # add by me

        # print(shipping_address)
        ctx['shipping_method'] = method
        shipping_charge = method.calculate(self.request.basket)
        ctx['shipping_charge'] = shipping_charge
        if method.is_discounted:
            excl_discount = method.calculate_excl_discount(self.request.basket)
            ctx['shipping_charge_excl_discount'] = excl_discount
        ctx['order_total'] = OrderTotalCalculator().calculate(self.request.basket, shipping_charge)
        return ctx
    
    def get_billing_address(self, basket):
        # print('get_billing_address')
        addr_data = self.checkout_session.new_billing_address_fields()
        addr_id = self.checkout_session.billing_user_address_id()
        if addr_data:
            # print('primo if get_billing_address')
            # Load address data into a blank shipping address model
            return BillingAddress(**addr_data)

        if addr_id:
            # print('secondo if get_billing_address')
            try:
                # print('try')
                address = UserAddress._default_manager.get(pk=addr_id)
            except UserAddress.DoesNotExist:
                # print('except try')
                # An address was selected but now it has disappeared.  This can
                # happen if the customer flushes their address book midway
                # through checkout.  No idea why they would do this but it can
                # happen.  Checkouts are highly vulnerable to race conditions
                # like this.
                return None
            else:
                # print('second else')
                # Copy user address data into a blank shipping address instance
                billing_addr = BillingAddress()
                address.populate_alternative_model(billing_addr)
                return billing_addr

    def get_form(self, form_class=None):
        if not form_class:
            form_class = self.get_form_class()
        shipping_address = self.get_shipping_address(basket=self.request.basket)
        billing_address = self.get_billing_address(basket=self.request.basket)
        if not billing_address:
            # populate with shipping address fields
            billing_address = BillingAddress()
            shipping_address.populate_alternative_model(billing_address)
        form = form_class(instance=billing_address, **self.get_form_kwargs())
        return form

    def get_available_addresses(self):
        # Include only addresses where the country is flagged as valid for
        # shipping. Also, use ordering to ensure the default address comes
        # first.
        return self.request.user.addresses.filter(
            country__is_shipping_country=True).order_by(
            '-is_default_for_shipping')

    def post(self, request, *args, **kwargs):
        # Check if a shipping address was selected directly (e.g. no form was
        # filled in)
        if self.request.user.is_authenticated and 'address_id' in self.request.POST:
            address = UserAddress._default_manager.get(
                pk=self.request.POST['address_id'], user=self.request.user)
            action = self.request.POST.get('action', None)
            if action == 'bill_to':
                # User has selected a previous address to bill to
                self.checkout_session.bill_to_user_address(address)
                return redirect(self.get_success_url())
            else:
                return HttpResponseBadRequest()
        else:
            return super().post(
                request, *args, **kwargs)
           

    def form_valid(self, form):
        # Store the address details in the session and redirect to next step
        address_fields = dict(
            (k, v) for (k, v) in form.instance.__dict__.items()
            if not k.startswith('_'))
        self.checkout_session.bill_to_new_address(address_fields)
        return super().form_valid(form)


class PlaceOrderView(PaymentDetailsView):
    s = {}

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        self.checkout_session = CheckoutSessionData(request)
        if request.method == 'POST':
            return self.post(request, *args, **kwargs)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        payload = request.body
        if 'paypal' in str(payload):
            self.request.session['payment_method'] = "paypal"
        return self.handle_checkout_session(self.request.session)

    def handle_checkout_session(self, session):
        basket = self.load_frozen_basket(
            self.request.session['frozen_basket_id'])

        if not basket:
            return HttpResponse(status=400)
        shipping_method_code = self.checkout_session.shipping_method_code(
            basket)
        submission = self.build_submission(basket=basket)
        submission['shipping_method'] = self.get_shipping_method(
            basket=basket, code=shipping_method_code, shipping_address=submission['shipping_address'])
        submission['shipping_charge'] = submission['shipping_method'].calculate(
            basket)
        submission['order_total'] = OrderTotalCalculator().calculate(
            basket, submission['shipping_charge'])
        submission['payment_kwargs']['amount'] = submission['order_total'].excl_tax

        self.submit(**submission)

        send_email_to_admin(obj=basket.order_set.first(), typology='order')
        self.s['checkout_order_id'] = basket.order_set.first().pk
        return HttpResponse(status=200)

    def build_submission(self, basket, **kwargs):
        submission = super().build_submission(**kwargs)

        submission['basket'] = basket
        submission['shipping_address'] = self.get_shipping_address(basket)
        submission['billing_address'] = self.get_billing_address(basket)
        submission['shipping_method'] = self.get_shipping_method(
            basket, self.get_shipping_address(basket))

        # Pass the user email so it can be stored with the order
        submission['order_kwargs']['guest_email'] = basket.owner.email
        submission['payment_kwargs']['amount'] = basket.total_incl_tax
        submission['payment_kwargs']['currency'] = basket.currency
        submission['user'] = basket.owner
        return submission

    def load_frozen_basket(self, basket_id):
        # Lookup the frozen basket that this txn corresponds to
        try:
            basket = Basket.objects.get(id=basket_id, status=Basket.FROZEN)
        except Basket.DoesNotExist:
            return None

        # Assign strategy to basket instance
        if Selector:
            basket.strategy = Selector().strategy(self.request)

        # Re-apply any offers
        Applicator().apply(basket, basket.owner, request=self.request)

        return basket

    def get_shipping_address(self, basket):

        if not basket.is_shipping_required():
            return None

        addr_data = self.checkout_session.new_shipping_address_fields()
        addr_id = self.checkout_session.shipping_user_address_id()

        if addr_data:
            # Load address data into a blank shipping address model
            return ShippingAddress(**addr_data)

        if addr_id:
            try:
                address = UserAddress._default_manager.get(pk=addr_id)
            except UserAddress.DoesNotExist:
                # An address was selected but now it has disappeared.  This can
                # happen if the customer flushes their address book midway
                # through checkout.  No idea why they would do this but it can
                # happen.  Checkouts are highly vulnerable to race conditions
                # like this.
                return None
            else:
                # Copy user address data into a blank shipping address instance
                shipping_addr = ShippingAddress()
                address.populate_alternative_model(shipping_addr)
                return shipping_addr

    def get_billing_address(self, basket):
        addr_data = self.checkout_session.new_billing_address_fields()
        addr_id = self.checkout_session.billing_user_address_id()
        if addr_data:
            # Load address data into a blank shipping address model
            return BillingAddress(**addr_data)

        if addr_id:
            try:
                address = UserAddress._default_manager.get(pk=addr_id)
            except UserAddress.DoesNotExist:
                # An address was selected but now it has disappeared.  This can
                # happen if the customer flushes their address book midway
                # through checkout.  No idea why they would do this but it can
                # happen.  Checkouts are highly vulnerable to race conditions
                # like this.
                return None
            else:
                # Copy user address data into a blank shipping address instance
                billing_addr = BillingAddress()
                address.populate_alternative_model(billing_addr)
                return billing_addr

    def get_shipping_method(self, basket, code, shipping_address=None):
        """
        Return the selected shipping method instance from this checkout session
        The shipping address is passed as we need to check that the method
        stored in the session is still valid for the shipping address.
        """
        methods = Repository().get_shipping_methods(
            basket=basket, user=self.request.user,
            shipping_addr=shipping_address, request=self.request)
        for method in methods:
            if method.code == code:
                return method

    def handle_payment(self, order_number, total, **kwargs):

        # Complete payment with Moneta - devo ricavare i porcoiddi di currency,
        # amount_allocated, amount_debited, reference. Controlla oscar.apps.payment.model

        # Record payment source and event
        source_type, is_created = SourceType.objects.get_or_create(
            name=self.request.session['payment_method'])
        source = Source(source_type=source_type,
                        currency=kwargs['currency'],
                        amount_allocated=kwargs['amount'],
                        amount_debited=kwargs['amount'])
        self.add_payment_source(source)
        self.add_payment_event('Settled', kwargs['amount'])

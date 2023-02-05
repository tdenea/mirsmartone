from oscar.apps.shipping import methods
from oscar.core import prices
from decimal import Decimal as D
from django.utils.translation import gettext_lazy as _


class StandardEurope(methods.FixedPrice):
    # Europa meno: Ungheria, Bulgaria, Estonia, Lettonia, Lituania, Romania
    code = 'standard-europe'
    name = _('Standard shipping Europe')
    time = _('%(days)s days') % {'days': '3 - 6'}
    charge_excl_tax = D('5.90')
    charge_incl_tax = D('5.90')

class StandardEurope2(methods.FixedPrice):
    # Ungheria, Bulgaria, Estonia, Lettonia, Lituania, Romania
    code = 'standard-europe2'
    name = _('Standard shipping Europe')
    time = _('%(days)s days') % {'days': '3 - 6'}
    charge_excl_tax = D('7.90')
    charge_incl_tax = D('7.90')

class StandardItaly(methods.FixedPrice):
    # Europa
    code = 'standard-italy'
    name = _('Standard shipping Italy')
    time = _('%(days)s days') % {'days': '2 - 4'}
    charge_excl_tax = D('3.90')
    charge_incl_tax = D('3.90')

class Free(methods.FixedPrice):
    code = 'free'
    name = _('Free shipping')
    time = '-'
    charge_excl_tax = D('0.00')
    charge_incl_tax = D('0.00')

class NoShipping(methods.FixedPrice):
    code = 'no-shipping'
    name = _('Shipping costs will be calculated after entering the delivery address')
    time = '-'
    charge_excl_tax = D('7.90')
    charge_incl_tax = D('7.90')

class StandardShipping(methods.FixedPrice):
    # Europa
    code = 'standard'
    name = _('Standard shipping')
    time = _('%(days)s days') % {'days': '2 - 4'}
    charge_excl_tax = D('15.00')
    charge_incl_tax = D('15.00')
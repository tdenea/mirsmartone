from django import template
from django.utils.translation import get_language
from wagtail.core.models import Page
from django.conf import settings
from django.db.models import Q
from django.contrib import messages, sessions
from django.utils.safestring import SafeString
import random
from oscar.core.loading import get_model
from home.models import *
from django.utils.safestring import mark_safe
from django.utils.text import normalize_newlines
import time
from django.contrib.sites.models import Site
import re
from decimal import Decimal as D

Product = get_model('catalogue', 'Product')

register = template.Library()

@register.simple_tag#(takes_context=True)
def list_hreflang(id):
    
    url_list = {}
    try:
        if BasePage.objects.filter(Q(id=id)):
            page = BasePage.objects.filter(Q(id=id)).first()
        elif HomePage.objects.filter(Q(id=id)):
            page = HomePage.objects.filter(Q(id=id)).first()
        elif TextualPage.objects.filter(Q(id=id)):
            page = TextualPage.objects.filter(Q(id=id)).first()

        if page.is_leaf() and not page.get_parent().specific.slug == 'home':
            url_list['en'] = '/en/' + page.get_parent().specific.slug + '/' + page.slug + '/'
            url_list['it'] = '/it/' + page.get_parent().specific.slug_it + '/' + page.slug_it + '/'
            url_list['de'] = '/de/' + page.get_parent().specific.slug_de + '/' + page.slug_de + '/'
            url_list['fr'] = '/fr/' + page.get_parent().specific.slug_fr + '/' + page.slug_fr + '/'
            url_list['es'] = '/es/' + page.get_parent().specific.slug_es + '/' + page.slug_es + '/'
        else:
            if page.slug == 'home':
                url_list['en'] = '/en/'
                url_list['it'] = '/it/'
                url_list['de'] = '/de/'
                url_list['fr'] = '/fr/'
                url_list['es'] = '/es/'
            else:
                url_list['en'] = '/en/' + page.slug + '/'
                url_list['it'] = '/it/' + page.slug_it + '/'
                url_list['de'] = '/de/' + page.slug_de + '/'
                url_list['fr'] = '/fr/' + page.slug_fr + '/'
                url_list['es'] = '/es/' + page.slug_es + '/'
        return url_list
    except:
        return ''

@register.simple_tag(takes_context=True)
def get_parameters(context, except_field):
    """
    Renders current get parameters except for the specified parameter
    """
    getvars = context['request'].GET.copy()
    getvars.pop(except_field, None)
    if len(getvars.keys()) > 0:
        return "%s&" % getvars.urlencode()

    return ''
    
@register.filter
def get_value_in_qs(queryset, key):
    return list(queryset.values_list(key, flat=True))


def strip_lang(path):
    pattern = '^(/%s)/' % get_language()
    match = re.search(pattern, path)
    if match is None:
        return path
    return path[match.end(1):]

register.filter('strip_lang', strip_lang)


@register.filter
def shuffle(arg):
    tmp = list(arg)[:]
    random.shuffle(tmp)
    return tmp

@register.filter
def split(value, separator=' '):
    return value.split(separator)

@register.filter
def seconds_to_time(value):
    try:
        return time.strftime('%M:%S', time.gmtime(int(value)))
    except Exception as e:
        print(e)
    return value


@register.simple_tag
def get_slug_by_id(id):
    page = None
    url_path = ''
    try:
        page = Page.objects.get(id=id)
        if page.get_parent() and not page.get_parent().specific.slug == 'home':
            # depth 1 = root
            # depth 2 = homepage
            # depth 3 = pagina interna
            # depth 4 = pagina interna / pagina interna
            # depth 5 = pagina interna / pagina interna / pagina interna
            # depth 6 = pagina interna / pagina interna / pagina interna / pagina interna
            ancestors = page.get_ancestors()
            if page.depth == 4:
                # url a due livelli
                url_path = '/' + page.get_parent().specific.translated_slug + '/' + page.specific.translated_slug + '/'
            elif page.depth == 5:
                # url a tre livelli
                url_path = '/' + ancestors[2].specific.translated_slug + '/' + ancestors[3].specific.translated_slug + '/' + page.specific.translated_slug + '/'
            elif page.depth == 6:
                # url a tre livelli
                url_path = '/' + ancestors[2].specific.translated_slug + '/' + ancestors[3].specific.translated_slug + '/' + ancestors[4].specific.translated_slug + '/' + page.specific.translated_slug + '/'
            elif page.depth == 7:
                # url a quattro livelli
                url_path = '/' + ancestors[2].specific.translated_slug + '/' + ancestors[3].specific.translated_slug + '/' + ancestors[4].specific.translated_slug + '/' + ancestors[5].specific.translated_slug + '/' + page.specific.translated_slug + '/'
        else:
            url_path = '/' + page.specific.translated_slug + '/'
    except:
        pass
    return url_path

def remove_newlines(text):
    """
    Removes all newline characters from a block of text.
    """
    # First normalize the newlines using Django's nifty utility
    normalized_text = normalize_newlines(text)
    # Then simply remove the newlines like so.
    return mark_safe(normalized_text.replace('\n', ' '))

register.filter('remove_newlines', remove_newlines)

@register.simple_tag
def get_current_site():
    current_site = Site.objects.get_current()
    return current_site


@register.simple_tag
def get_smartone():
    product = None
    try:
      product = Product.objects.filter(title='Smart One').first()
    except Exception as e:
      print(e)
      pass
    return product

@register.simple_tag
def get_smartoneoxi():
    product = None
    try:
      product = Product.objects.filter(title='Smart One Oxi').first()
    except Exception as e:
      print(e)
      pass
    return product

@register.simple_tag
def get_set_turbina():
    product = None
    try:
      product = Product.objects.filter(upc='set_turbina_boccaglio').first()
    except Exception as e:
      print(e)
      pass
    return product

@register.simple_tag
def get_one_and_set(request):
    set_turbina = None
    one = None
    total_one = D(0)
    # Get set turbina
    try:
      set_turbina = Product.objects.filter(upc__icontains='set_turbina_boccaglio', is_public=True).first()
    except Exception as e:
      print(e)
      pass
    # Get Smartone
    try:
      one = Product.objects.filter(upc='smartone', is_public=True).first()
    except Exception as e:
      print(e)
      pass
    if set_turbina and one:
        # set turbina Price
        set_turbina_session = request.strategy.fetch_for_parent(set_turbina) if set_turbina.is_parent else request.strategy.fetch_for_product(set_turbina)
        set_turbina_price = set_turbina_session.price.incl_tax if set_turbina_session.price.is_tax_known else set_turbina_session.price.excl_tax
        # Smartone Price
        one_session = request.strategy.fetch_for_parent(one) if one.is_parent else request.strategy.fetch_for_product(one)
        one_price = one_session.price.incl_tax if one_session.price.is_tax_known else one_session.price.excl_tax
        # SUM
        total_one = D(one_price+set_turbina_price)
    return total_one

@register.simple_tag
def get_oxi_and_set(request):
    set_turbina = None
    oxi = None
    total_oxi = D(0)
    # Get Set Turbina
    try:
      set_turbina = Product.objects.filter(upc__icontains='set_turbina_boccaglio', is_public=True).first()
    except Exception as e:
      print(e)
      pass
    # Get Oxi
    try:
      oxi = Product.objects.filter(upc='smartoneoxi', is_public=True).first()
    except Exception as e:
      print(e)
      pass
    if set_turbina and oxi:
        # Cset turbina Price
        set_turbina_session = request.strategy.fetch_for_parent(set_turbina) if set_turbina.is_parent else request.strategy.fetch_for_product(set_turbina)
        set_turbina_price = set_turbina_session.price.incl_tax if set_turbina_session.price.is_tax_known else set_turbina_session.price.excl_tax
        # Smartoneoxi Price
        oxi_session = request.strategy.fetch_for_parent(oxi) if oxi.is_parent else request.strategy.fetch_for_product(oxi)
        oxi_price = oxi_session.price.incl_tax if oxi_session.price.is_tax_known else oxi_session.price.excl_tax
        # SUM
        total_oxi = D(oxi_price+set_turbina_price)
    return total_oxi


@register.simple_tag
def get_price_smartone(request):
    smartone = None
    price = None
    # Get smartone
    try:
      smartone = Product.objects.filter(title='Smart One', is_public=True).first()
    except Exception as e:
      print(e)
      pass
    if smartone:
        # smartone Price
        smartone_session = request.strategy.fetch_for_parent(smartone) if smartone.is_parent else request.strategy.fetch_for_product(smartone)
        smartone_price = smartone_session.price.incl_tax if smartone_session.price.is_tax_known else smartone_session.price.excl_tax
        # SUM
        price = D(smartone_price)
    return price


@register.simple_tag
def get_price_smartoneoxi(request):
    smartoneoxi = None
    price = None
    # Get smartoneoxi
    try:
      smartoneoxi = Product.objects.filter(title='Smart One Oxi', is_public=True).first()
    except Exception as e:
      print(e)
      pass
    if smartoneoxi:
        # smartoneoxi Price
        smartoneoxi_session = request.strategy.fetch_for_parent(smartoneoxi) if smartoneoxi.is_parent else request.strategy.fetch_for_product(smartoneoxi)
        smartoneoxi_price = smartoneoxi_session.price.incl_tax if smartoneoxi_session.price.is_tax_known else smartoneoxi_session.price.excl_tax
        # SUM
        price = D(smartoneoxi_price)
    return price

@register.simple_tag
def get_price_set_turbina(request):
    set_turbina = None
    price = None
    # Get set_turbina
    try:
      set_turbina = Product.objects.filter(upc='set_turbina_boccaglio', is_public=True).first()
    except Exception as e:
      print(e)
      pass
    if set_turbina:
        # set_turbina Price
        set_turbina_session = request.strategy.fetch_for_parent(set_turbina) if set_turbina.is_parent else request.strategy.fetch_for_product(set_turbina)
        set_turbina_price = set_turbina_session.price.incl_tax if set_turbina_session.price.is_tax_known else set_turbina_session.price.excl_tax
        # SUM
        price = D(set_turbina_price)
    return price

def replace_commas(string):
    return str(string).replace(',', '.')
register.filter('replace_commas', replace_commas)


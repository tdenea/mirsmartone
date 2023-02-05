# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.contrib import messages, sessions
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core import serializers, management
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.conf import settings
from django.template import Context, loader, Template
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import requests
from wagtail.core.models import Page
from cities_light.models import Country, SubRegion
from oscar.core.loading import get_model
import re
import urllib
import urllib.request
import json
from .models import *

Product = get_model('catalogue', 'Product')

from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID

# Integrazione con Mailchimp
def subscribe_mailchimp(email):
    """
     Contains code handling the communication to the mailchimp api
     to create a contact/member in an audience/list.
    """

    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })

    member_info = {
        "email_address": email,
        "status": "subscribed",
        "tags": ["Website"],
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))

# Active language if is supported
def active_language_supported(language, request):
    for key, lang in settings.LANGUAGES:
        if key == language:
            translation.activate(language)
            request.session[translation.LANGUAGE_SESSION_KEY] = language

# Search page by slug into all languages
def get_page_by_all_languages(slug):
    print('get_page_by_all_languages')
    page = None
    for key, lang in settings.LANGUAGES:
        if not key == 'en':
          query = {'slug_'+key : slug}
        else:
          query = {'slug' : slug}

        if BasePage.objects.filter(**query):
            page = BasePage.objects.get(**query)
            break
        elif TextualPage.objects.filter(**query):
            page = TextualPage.objects.get(**query)
            break
    return page

# Search page by slug into all languages
def get_page_by_all_languages_into_parent(slug, parent):
    page = None
    if hasattr(parent, 'get_children') and parent.get_children().count():
        for item in parent.get_children().all():
            if item.specific.slug == slug \
                or item.specific.slug_it == slug \
                or item.specific.slug_fr == slug \
                or item.specific.slug_de == slug \
                or item.specific.slug_es == slug:
                page = item.specific
                break
    return page

def get_page_by_default_language(slug):
    # Fatto questa funzione per velocizzare la ricerca delle pagine in lingua italiana (default)
    page = None
    try:
        page=Page.objects.get(slug=slug, depth=3).specific
    except Exception as e:
        print(e)
    return page

def get_page_by_language(language, slug):
    # per tutte le pagine
    query = {'slug' : slug}
    page = None
    if not language == 'en':
      query = {'slug_'+language : slug}
    else:
      query = {'slug' : slug}
    # Cerco su tutti i models
    if BasePage.objects.filter(**query):
        page = BasePage.objects.get(**query)
    elif TextualPage.objects.filter(**query):
        page = TextualPage.objects.get(**query)
    return page

def can_view_page(request, page):
    # Verifico all'interno di tutte le permissioni associate a questa pagina
    for pvr in page.get_view_restrictions():
        # Se una delle permissioni accetta la request, vuol dire che l'utente ha permesso per vederla
        if pvr.accept_request(request):
            return True
    return False

def slug_view(request, slug='home'):
    language_request = translation.get_language_from_request(request, check_path=True)
    
    active_language_supported(language_request, request)

    full_path = request.path[1:-1].split('/')
    full_path.pop(0)
    full_path.reverse()
    # Dichiaro variabile parent iniziale 
    parent_page = None
    # Se la pagina ha un parent, prendo prima il padre per poi prendere la pagina corretta
    if len(full_path) > 1:
        parent_page = get_page_by_all_languages(full_path[1])
        page=get_page_by_all_languages_into_parent(slug, parent_page)
    else:
        if language_request=='en':
            page = get_page_by_default_language(slug)
            if not page:
                page = get_page_by_all_languages(slug)
        else:
            page = get_page_by_language(language_request, slug)
    # try to search a page into all languages
    if not page:
        page = get_page_by_all_languages(slug)
    # If page not exists
    if not page:
        return render(request, '404.html', status=404)
    
    # Verifico permissions
    if page.get_view_restrictions().exists():
        if not can_view_page(request, page):
            return render(request, '403.html', status=403)

    template = page.get_template(request)
    context = page.get_context(request)

    context['seo_title'] = page.translated_seo_title
    context['search_description'] = page.translated_search_description
    context['title'] = page.translated_title
    context['child'] = page.is_leaf()

    try:
        if not page.live and not request.user.is_superuser:
            return render(request, '404.html', status=404)
        else:
            url_path = ''
            if page.get_parent() and not page.get_parent().specific.slug == 'home':
                # depth 1 = root
                # depth 2 = homepage
                # depth 3 = pagina interna
                # depth 4 = pagina interna / pagina interna
                # depth 5 = pagina interna / pagina interna / pagina interna
                # depth 6 = pagina interna / pagina interna / pagina interna / pagina interna
                ancestors = page.get_ancestors()
                if page.depth == 3:
                    # url senza livelli
                    url_path = '/' + language_request + '/' + page.translated_slug + '/'
                if page.depth == 4:
                    # url a due livelli
                    url_path = '/' + language_request + '/' + page.get_parent().specific.translated_slug + '/' + page.translated_slug + '/'
                elif page.depth == 5:
                    # url a tre livelli
                    url_path = '/' + language_request + '/' + ancestors[2].specific.translated_slug + '/' + ancestors[3].specific.translated_slug + '/' + page.translated_slug + '/'
                elif page.depth == 6:
                    # url a tre livelli
                    url_path = '/' + language_request + '/' + ancestors[2].specific.translated_slug + '/' + ancestors[3].specific.translated_slug + '/' + ancestors[4].specific.translated_slug + '/' + page.translated_slug + '/'
                elif page.depth == 7:
                    # url a quattro livelli
                    url_path = '/' + language_request + '/' + ancestors[2].specific.translated_slug + '/' + ancestors[3].specific.translated_slug + '/' + ancestors[4].specific.translated_slug + '/' + ancestors[5].specific.translated_slug + '/' + page.translated_slug + '/'
                context['act_page'] = url_path
                if request.path != context['act_page']:
                    return HttpResponseRedirect(url_path)
            else:
                context['act_page'] = '/' + language_request + '/' + page.translated_slug + '/'
                if request.path != context['act_page']:
                    return HttpResponseRedirect('/' + language_request + '/' + page.translated_slug + '/')
        return render(request, template, context)
    except Exception as e:
        print(e)
        try:
            if not page.live and not request.user.is_superuser:
                return render(request, '404.html', status=404)
            else:
                if page.is_leaf() and not page.get_parent().specific.slug == 'home':
                    return HttpResponseRedirect('/' + page.get_parent().specific.translated_slug + '/' + page.translated_slug)
                else:
                    return HttpResponseRedirect(reverse('slug', kwargs={'slug': page.translated_slug}))
        except Exception as e:
            print('except2')
            print(e)
            return render(request, '404.html', status=404)

def get_recipients_by_country(country):
    recipients = []
    # Lista 1 = ['Australia', 'India', 'Colombia', 'Argentina', 'Mexico', 'Saudi Arabia', 'Chile', 'United Arab Emirates', 'Peru', 'Ecuador', 'Qatar', 'Israel', 'Dominican Republic', 'Paraguay', 'Jordan', 'Bahrain', 'Iraq', 'Kuwait', 'Egypt', 'Libya', 'Oman', 'Yemen', 'Bolivia', 'Venezuela', 'Myanmar', 'Palestine, State of', 'Honduras', 'Lebanon', 'Guatemala', 'Virgin Islands (British)', 'Costa Rica', 'El Salvador', 'Nicaragua', 'Panama', 'Syria', 'Trinidad and Tobago', 'Australia', 'New Zealand', 'Pakistan', 'Nepal', 'Bangladesh', 'Sri Lanka']
    if country in ['AU','IN','CO','AR','MX','SA','CL','AE','PE','EC','QA','IL','DO','PY','JO','BH','IQ','KW','EG','LY','OM','YE','BO','VE','MM','PS','HN','LB','GT','VG','CR','SV','NI','PA','SY','TT','AU','NZ','PK','NP','BD','LK']:
        if settings.IS_PRODUCTION:
            recipients.append('Luigi Ottaviani <luigi.o@spirometry.com>')
        else:
            recipients.append('Lucia Conti <lucia.unbit@gmail.com>')
    # Lista 2 = ['Hungary', 'Austria', 'Kenya', 'Finland', 'Tanzania', 'Nigeria', 'Maldives', 'Switzerland', 'Uganda', 'Malawi', 'Mauritius', 'Zimbabwe', 'Bhutan', 'Botswana', 'Ethiopia', 'Iceland', 'Angola', 'Burundi', 'Cabo Verde', 'Chad', 'Comoros', 'Eritrea', 'eSwatini', 'Gambia', 'Ghana', 'Djibouti', 'Guinea', 'Equatorial Guinea', 'Guinea-Bissau', 'Lesotho', 'Liberia', 'Madagascar', 'Namibia', 'Central African Republic', 'Rwanda', 'Seychelles', 'Sierra Leone', 'Somalia', 'Sudan', 'South Sudan', 'Zambia', 'South Africa']
    elif country in ['HU','AT','KE','FI','TZ','NG','MV','CH','UG','MW','MU','ZW','BT','BW','ET','IS','AO','BI','CV','TD','KM','ER','SZ','GM','GH','DJ','GN','GQ','GW','LS','LR','MG','NA','CF','RW','SC','SL','SO','SD','SS','ZM','ZA']:
        if settings.IS_PRODUCTION:
            recipients.append('Elisa Salvi <elisa.s@spirometry.com>')
        else:
            recipients.append('Caio Jhonny <caiojhonnyp@gmail.com>')
    # Lista 3 = ['Brazil', 'China', 'Sweden', 'Canada', 'Poland', 'Norway', 'Indonesia', 'Denmark', 'Thailand', 'Taiwan', 'Georgia', 'Singapore', 'Malaysia', 'Hong Kong', 'Japan', 'Mongolia', 'Vietnam', 'Philippines', 'Laos', 'South Korea']
    elif country in ['BR','CN','SE','CA','PL','NO','ID','DK','TH','TW','GE','SG','MY','HK','JP','MN','VN','PH','LA','KR']:
        if settings.IS_PRODUCTION:
            recipients.append('Katherina Zavatta <katherina.z@spirometry.com>')
        else:
            recipients.append('Caio Jhonny <caiojhonnyp@gmail.com>')
    # Lista 4 = ['Romania', 'Greece', 'Iran', 'Spain', 'Turkey', 'Ireland', 'Bulgaria', 'Croatia', 'Serbia', 'Lithuania', 'Portugal', 'Cyprus', 'Czech Republic', 'Slovakia', 'Bosnia and Herzegovina', 'Albania', 'Moldova', 'Macedonia', 'Slovenia', 'Latvia', 'Malta', 'Estonia', 'Kosovo', 'Russia', 'Ukraine', 'Netherlands', 'Kazakhstan', 'Azerbaijan', 'Armenia', 'Uzbekistan']
    elif country in ['RO','GR','IR','ES','TR','IE','BG','HR','RS','LT','PT','CY','CZ','SK','BA','AL','MD','MK','SI','LV','MT','EE','XK','RU','UA','NL','KZ','AZ','AM','UZ']:
        if settings.IS_PRODUCTION:
            recipients.append('Alessandra Dorsa <alessandra.d@spirometry.com>')
        else:
            recipients.append('Caio Jhonny <caiojhonnyp@gmail.com>')
    # Lista 5 - ['Germany', 'United Kingdom']
    elif country in ['DE', 'GB']:
        if settings.IS_PRODUCTION:
            recipients.append('Roberta Di Pinto <roberta.d@spirometry.com>')
            recipients.append('Gerda Van Houts <gerda.v@spirometry.com>')
        else:
            recipients.append('Caio Jhonny <caiojhonnyp@gmail.com>')
    # Lista 6 - ['Belgium','Côte d\'Ivoire','Mali','Morocco','Senegal','Togo','Tunisia','Algeria','France']
    elif country in ['BE','CI','ML','MA','SN','TG','TN','DZ','FR']:
        if settings.IS_PRODUCTION:
            recipients.append('MIR France <secretariat@lamirau.com>')
        else:
            recipients.append('Caio Jhonny <caiojhonnyp@gmail.com>')
    # Lista 7 - ['United States of America', 'Puerto Rico']
    elif country in ['US', 'PR']:
        if settings.IS_PRODUCTION:
            recipients.append('Dale Novy <dale.n@spirometry.com>')
        else:
            recipients.append('Caio Jhonny <caiojhonnyp@gmail.com>')
    # Lista 8 - ['Italy']
    elif country in ['IT']:
        if settings.IS_PRODUCTION:
            recipients.append('Raniero Citarella <citarella.r@spirometry.com>')
            recipients.append('Sara Tosi Brandi <sara.t@spirometry.com>')
            # recipients.append('Laura Precetti <laura.p@spirometry.com>')
            recipients.append('Claudia Marata <claudia.m@spirometry.com>')
        else:
            recipients.append('Caio Jhonny <caiojhonnyp@gmail.com>')
    return recipients


def send_email_to_admin(obj, typology='contact', attachments=None, file=None):
    site = Site.objects.get_current()
    
    if typology == 'customer_service':
        template = "email/new_customer_service.html"
        subject = _("New customer service request from ") + obj.name + " " + obj.surname
        EMAIL_RECIPIENTS = settings.EMAIL_RECIPIENTS_CUSTOMER_SERVICE
        EMAIL_RECIPIENTS_HIDDEN = []
    elif typology == "order":
        EMAIL_RECIPIENTS = settings.EMAIL_ORDERS
        EMAIL_RECIPIENTS_HIDDEN = []
        subject = _("New Order n." + obj.number + " from website")
        template = "communication/emails/new_order.html"
        context = {"order": obj, 'site': site}
    else:
        template = "email/new_contact.html"
        subject = _('Richiesta Informazioni Utente')
        EMAIL_RECIPIENTS = settings.EMAIL_RECIPIENTS
        EMAIL_RECIPIENTS_HIDDEN = []

    context = {"obj": obj, "site":site}
    html = loader.get_template(template)
    html_content = html.render(context)

    email_to_sent = EmailMessage(subject, html_content, settings.EMAIL_SENDER, EMAIL_RECIPIENTS, reply_to=[obj.email], bcc=EMAIL_RECIPIENTS_HIDDEN)
    email_to_sent.content_subtype = "html"

    if attachments:
        email_to_sent.attach(file.name, file.read())

    email_to_sent.send()

def send_email_to_user(obj, email, mail_type="contact"):
    site = Site.objects.get_current()
    if mail_type == 'newsletter':
        oggetto = _("Ti sei iscritto alla newsletter di MIR Smart One")
        template = "email/newsletter_user.html"
    else:
        oggetto = _("Grazie per aver contattato MIR Smart One")
        template = "email/contact_user.html"

    EMAIL_RECIPIENTS = [email]
    context = {"obj": obj, "site":site}
    html = loader.get_template(template)
    html_content = html.render(context)

    email_to_sent = EmailMessage(oggetto, html_content, settings.EMAIL_SENDER, EMAIL_RECIPIENTS)
    email_to_sent.content_subtype = "html"
    email_to_sent.send()

def save_newsletter(request):
    ''' Begin reCAPTCHA validation '''
    recaptcha_response = request.POST.get('recaptcha_response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode("utf-8")
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req, data=data)
    result = json.load(response)
    ''' End reCAPTCHA validation '''

    if result['success']:    
        if request.method == 'POST':
            site = get_current_site(request)
            email = request.POST.get('email')
            privacy = request.POST.get('privacy', '')

            if privacy == 'true':
                privacy = True
            else:
                privacy = False
                return JsonResponse({"error":1, "msg":"Compila tutti i campi"})

            # if FormNewsletter.objects.filter(email=email).exists():
            #     return JsonResponse({"error":2, "msg":"Ti sei già scritto alla newsletter utilizzando questo indirizzo email."})

            try:
                new_obj, created = FormNewsletter.objects.update_or_create(email=email)

                # Save to mailchimp
                subscribe_mailchimp(email)

                send_email_to_user(new_obj, email=email, mail_type="newsletter")
                return JsonResponse({"error":0, "msg":"Inviato!"})
            except Exception as e:
                print(e)
                return JsonResponse({"error":1, "msg":"Compila tutti i campi"})
    else:
        return JsonResponse({"error":2, 'msg' : _('ReCAPTCHA non valido. Riprova.')})

def save_contact(request):
    ''' Begin reCAPTCHA validation '''
    recaptcha_response = request.POST.get('recaptcha_response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode("utf-8")
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req, data=data)
    result = json.load(response)
    ''' End reCAPTCHA validation '''

    if result['success']:
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            message = request.POST.get('message')
            privacy = request.POST.get('privacy')
            newsletter = request.POST.get('newsletter')
            print(name)
            print(phone)
            print(email)
            print(message)
            print(privacy)
            print(newsletter)
            if privacy == 'true':
                privacy = True
            else:
                privacy = False
            
            if newsletter == 'true':
                newsletter = True

                # Save to mailchimp
                subscribe_mailchimp(email)
            else:
                newsletter = False

            try:
                new_obj = FormContact(name=name, phone=phone, email=email, message=message, privacy=privacy, newsletter=newsletter)
                new_obj.save()
                
                send_email_to_admin(new_obj, typology='contact')
                send_email_to_user(new_obj, email=email, mail_type="contact")
                return JsonResponse({"error":0, "msg":_("Inviato!")})
            except Exception as e:
                print(e)
                return JsonResponse({"error":1, "msg":_(_("Compila tutti i campi"))})
    else:
        return JsonResponse({"error":2, 'msg' : _('ReCAPTCHA non valido. Riprova.')})


def save_customer_service(request):
    ''' Begin reCAPTCHA validation '''
    recaptcha_response = request.POST.get('recaptcha_response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode("utf-8")
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req, data=data)
    result = json.load(response)
    ''' End reCAPTCHA validation '''

    if result['success']:
        if request.method == 'POST':
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            message = request.POST.get('message')
            privacy = request.POST.get('privacy')
            
            if privacy == 'on':
                privacy = True
            else:
                privacy = False

            try:
                new_obj = FormCustomerService(name=name, surname=surname, phone=phone, email=email, message=message, privacy=privacy)
                new_obj.save()
                
                send_email_to_admin(new_obj, typology='customer_service')
                return JsonResponse({"error":0, "msg":_("Inviato!")})
            except Exception as e:
                print(e)
                return JsonResponse({"error":1, "msg":_("Compila tutti i campi")})
    else:
        return JsonResponse({"error":2, 'msg' : _('ReCAPTCHA non valido. Riprova.')})

@login_required
def get_states(request):
    if request.method == 'POST':
        value = request.POST.get('value')
        try:
            country = Country.objects.get(code2=value)
            states = list(country.subregion_set.all().exclude(region__name__in=settings.EXCLUDED_REGIONS).values('name'))
            return JsonResponse({"error":0, "content": states})
        except Exception as e:
            print(e)
            return JsonResponse({"error":1, "msg":_("Country not found")})
    else:
        return JsonResponse({"error":2, 'msg' : _('GET Method not allowed.')})

@login_required
def get_cities(request):
    if request.method == 'POST':
        value = request.POST.get('value')
        try:
            subregion = SubRegion.objects.get(name=value)
            cities = list(subregion.city_set.all().exclude(subregion__region__name__in=settings.EXCLUDED_REGIONS).values('name'))
            return JsonResponse({"error":0, "content": cities})
        except Exception as e:
            print(e)
            return JsonResponse({"error":1, "msg":_("SubRegion not found")})
    else:
        return JsonResponse({"error":2, 'msg' : _('GET Method not allowed.')})

def add_both_one(request):
    basket = request.basket
    
    # Get Smart One
    try:
      smartone = Product.objects.filter(title='Smart One', is_public=True).first()
    except Exception as e:
      print(e)
      pass
    # Get set_turbin
    try:
      set_turbina = Product.objects.filter(upc='set_turbina_boccaglio', is_public=True).first()
    except Exception as e:
      print(e)
      pass

    if smartone:
        basket.add_product(smartone)
    
    if set_turbina:
        basket.add_product(set_turbina)
    
    return JsonResponse({"error":0})

def add_both_oxi(request):
    basket = request.basket
    
    # Get Smart One OXI
    try:
      smartoneoxi = Product.objects.filter(title='Smart One Oxi', is_public=True).first()
    except Exception as e:
      print(e)
      pass
    # Get set_turbin
    try:
      set_turbina = Product.objects.filter(upc='set_turbina_boccaglio', is_public=True).first()
    except Exception as e:
      print(e)
      pass

    if smartoneoxi:
        basket.add_product(smartoneoxi)
    
    if set_turbina:
        basket.add_product(set_turbina)
    
    return JsonResponse({"error":0})
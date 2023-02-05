import decimal
import json
import math
from datetime import timezone
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template
from sorl.thumbnail import get_thumbnail
from django.utils import translation
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from decimal import Decimal as D
from django.http import JsonResponse
from oscar.core.loading import get_model
# from oscar.apps.basket.models import Line
import datetime
from notify_user.models import AbandonedCartMailHistory
from user.models import User

Product = get_model('catalogue', 'Product')
Basket = get_model('basket', 'Basket')
Line = get_model("basket", "Line")

def get_translation_in(language, s):
    with translation.override(language):
        return translation.gettext(s)

def commanFun(item):
    try:
        user_data = User.objects.get(id=item.owner_id)
    except User.DoesNotExist:
        user_data = None
    if user_data:
        productInfo = []
        basket_products = Line.objects.filter(basket_id=item.id)
        productArrayData = []
        total_rate = 0
        currency = ""
        for line in basket_products:
            if not line.product.structure == 'standalone' and line.product.parent:
                img = get_thumbnail(line.product.parent.primary_image().original, '64x90', quality=99)
            else:
                img = get_thumbnail(line.product.primary_image().original, '64x90', quality=99)
            productArrayData.append({
                'product':line.product.id,
                'quantity':line.quantity,
                "price_incl_tax":str(line.price_incl_tax),
                "currency":line.price_currency
            })
            subData = {}
            subData["name"] = line.product.title
            subData["price"] = line.price_incl_tax
            subData["img"] = img.url
            subData["currency"] = line.price_currency
            currency = line.price_currency
            subData["quantity"] = line.quantity
            subData["total_price"] = line.quantity * line.price_incl_tax
            productInfo.append(subData)
            total_rate = total_rate + (line.quantity * line.price_incl_tax)
        total_rate = total_rate
        d={
            'products':productInfo,
            "user_data":user_data,
            "total_rate":total_rate,
            "currency":currency,
            "site": Site.objects.get_current().domain,
            "productIDArray":json.dumps(productArrayData),
            'exists':True
        }
        return d;
    else:
        d={'exists':False}
        return d;

def get_abandoned_cart():
    get_time = datetime.datetime.now(timezone.utc)
    abandoned_cart_data = Basket.objects.filter(status="Open")
    submitted_cart_data = Basket.objects.filter(status="Submitted")
    basket_data = []
    for item in abandoned_cart_data:
        line_data_count = Line.objects.filter(basket_id=item.id).count()
        line_data = Line.objects.filter(basket_id=item.id)
        productIDArray = []
        productArrayData = []
        if line_data_count > 0:
            for product in line_data:
                productIDArray.append(product.product.id)
                productArrayData.append({
                    'product': product.product.id,
                    'quantity': product.quantity,
                    "price_incl_tax": str(product.price_incl_tax),
                    "currency": product.price_currency
                })
            hour3mailHistoryData = AbandonedCartMailHistory.objects\
                .filter(basket_id=item.id,history_status="open").count()
            if hour3mailHistoryData > 0:
                mailHistoryData = AbandonedCartMailHistory.objects\
                    .filter(basket_id=item.id,history_status="open").first()
                productArray = json.loads(mailHistoryData.product_history)
                productIds = []
                for p in productArray:
                    productIds.append(p["product"])
                if set(productIDArray) == set(productIds):
                    time_diff_3hours = get_time - mailHistoryData.update_time
                    hour_diff_3hours = math.floor((math.floor(time_diff_3hours.total_seconds()) / 60) / 60)
                    if hour_diff_3hours >= 3:
                        hour3mailHistoryDataCount = AbandonedCartMailHistory.objects\
                            .filter(basket_id=item.id,history_status="open")\
                            .exclude(first_reminder_mail_date=None).count()
                        if hour3mailHistoryDataCount > 0:
                            time_diff_2day = get_time - mailHistoryData.update_time
                            hour_diff_2day = math.floor((math.floor(time_diff_2day.total_seconds()) / 60) / 60)
                            if hour_diff_2day >= 48:
                                day2mailHistoryDataCount = AbandonedCartMailHistory.objects\
                                    .filter(basket_id=item.id,history_status="open")\
                                    .exclude(second_reminder_mail_date=None).count()
                                if day2mailHistoryDataCount > 0:
                                    time_diff_7day = get_time - mailHistoryData.update_time
                                    hour_diff_7day = math.floor((math.floor(time_diff_7day.total_seconds()) / 60) / 60)
                                    if hour_diff_7day >= 168:
                                        day7mailHistoryDataCount = AbandonedCartMailHistory.objects\
                                            .filter(basket_id=item.id, history_status="open")\
                                            .exclude(third_reminder_mail_date=None).count()
                                        if day7mailHistoryDataCount > 0:
                                            pass
                                        else:
                                            basket_data.append({"basket": item, "mail_type": 3})
                                    else:
                                        pass
                                else:
                                    basket_data.append({"basket": item, "mail_type": 2})
                        else:
                            basket_data.append({"basket": item, "mail_type": 1})
                    else:
                        pass
                else:
                    try:
                        user_data = User.objects.get(id=item.owner_id)
                    except User.DoesNotExist:
                        user_data = None
                    AbandonedCartMailHistory.objects.filter(basket_id=item.id,history_status="open")\
                        .update(history_status="close")
                    if user_data:
                        AbandonedCartMailHistory.objects.create(basket_id=item.id,user_id=item.owner_id,
                                                                history_status="open",product_history=json.dumps(productArrayData))
                    else:
                        pass
            else:
                try:
                    user_data = User.objects.get(id=item.owner_id)
                except User.DoesNotExist:
                    user_data = None
                if user_data:
                    AbandonedCartMailHistory.objects.create(basket_id=item.id, user_id=item.owner_id,
                                                            history_status="open",product_history=json.dumps(productArrayData))
                else:
                    pass
        else:
            historymailData = AbandonedCartMailHistory.objects.filter\
                (basket_id=item.id,history_status="open").count()
            if historymailData > 0:
                AbandonedCartMailHistory.objects.filter(basket_id=item.id)\
                    .update(history_status="close")
            else:
                pass
    if len(basket_data):
        for item in basket_data:
            d = commanFun(item["basket"])
            if(d['exists']):
                # Attivo la lingua dell'utente per fare l'invio
                translation.activate(d["user_data"].lang)
                mail_type = item["mail_type"]
                if int(mail_type) == 1:
                    html = get_template('customer/email/mail_abandoned_cart_1.html')
                    #subject = get_translation_in(d["user_data"].lang, "Hai un prodotto nel carrello")
                    subject = _("Hai un prodotto nel carrello")
                elif int(mail_type) == 2:
                    html = get_template('customer/email/mail_abandoned_cart_2.html')
                    #subject = get_translation_in(d["user_data"].lang, "Completa il tuo ordine!")
                    subject = _("Completa il tuo ordine!")
                else:
                    html = get_template('customer/email/mail_abandoned_cart_3.html')
                    subject = _("Non rinunciare al tuo Smart-One")
                html_content = html.render(d)
                email_to_sent = EmailMessage(subject, html_content, settings.EMAIL_SENDER,[d["user_data"].email])
                email_to_sent.content_subtype = "html"
                email_to_sent.send()
                if item["mail_type"] == 1:
                    AbandonedCartMailHistory.objects.filter(basket_id=item["basket"].id, history_status="open").update(
                        first_reminder_mail_date=datetime.datetime.now())
                elif item["mail_type"] == 2:
                    AbandonedCartMailHistory.objects.filter(basket_id=item["basket"].id,history_status="open").update(
                        second_reminder_mail_date=datetime.datetime.now())
                else:
                    AbandonedCartMailHistory.objects.filter(basket_id=item["basket"].id,history_status="open").update(
                        third_reminder_mail_date=datetime.datetime.now())
    for subItem in submitted_cart_data:
        AbandonedCartMailHistory.objects.filter(basket_id=subItem.id)\
            .update(history_status="submitted")
    #
    # return render(request, 'customer/email/mail_abandoned_cart_1.html', {})

def sent_mail_onclick(request):
    if request.method == 'GET':
        # Prendo lingua della request per poi riattivarla
        lang_request = translation.get_language_from_request(request, check_path=True)

        history_id = request.GET['history_id']
        mail_type = request.GET['mail_type']
        mailHistoryData = AbandonedCartMailHistory.objects.get(id=history_id);
        abandoned_cart_data = Basket.objects.get(id=mailHistoryData.basket_id)
        try:
            user_data = User.objects.get(id=abandoned_cart_data.owner_id)
        except User.DoesNotExist:
            user_data = None
        if user_data:
            # Attivo la lingua dell'utente per fare l'invio
            translation.activate(user_data.lang)
            productInfo = []
            productIDArray = json.loads(mailHistoryData.product_history)
            total_rate = 0
            currency = ""
            for product in productIDArray:
                prodObj = Product.objects.get(id=product["product"])
                if not prodObj.structure == 'standalone' and prodObj.parent:
                    img = get_thumbnail(prodObj.parent.primary_image().original, '64x90', quality=99)
                else:
                    img = get_thumbnail(prodObj.primary_image().original, '64x90', quality=99)
                subData = {}
                subData["name"] = prodObj.title
                subData["price"] = decimal.Decimal(product["price_incl_tax"])
                subData["img"] = img.url
                subData["currency"] = product["currency"]
                currency = product["currency"]
                subData["quantity"] = product["quantity"]
                subData["get_absolute_url"] = prodObj.get_absolute_url()
                subData["total_price"] = product["quantity"] * decimal.Decimal(product["price_incl_tax"])
                productInfo.append(subData)
                total_rate = total_rate + (product["quantity"] * decimal.Decimal(product["price_incl_tax"]))
            total_rate = total_rate
            d = {
                'products': productInfo,
                "user_data": user_data,
                "total_rate": total_rate,
                "currency": currency,
                "site": Site.objects.get_current().domain,
                "productIDArray": productIDArray,
                'exists': True
            }
        else:
            d = {'exists': False}

        if int(mail_type) == 1:
            html = get_template('customer/email/mail_abandoned_cart_1.html')
            #subject = get_translation_in(user_data.lang, "Hai un prodotto nel carrello")
            subject = _("Hai un prodotto nel carrello")
        elif int(mail_type) == 2:
            html = get_template('customer/email/mail_abandoned_cart_2.html')
            #subject = get_translation_in(user_data.lang, "Completa il tuo ordine!")
            subject = _("Completa il tuo ordine!")
        else:
            html = get_template('customer/email/mail_abandoned_cart_3.html')
            subject = _("Non rinunciare al tuo Smart-One")

        html_content = html.render(d)
        email_to_sent = EmailMessage(subject, html_content, settings.EMAIL_SENDER,[d["user_data"].email])
        email_to_sent.content_subtype = "html"
        email_to_sent.send()
        data = {
            "message": "Reminder Mail Successfully Sent"
        }
        # Dopo l'invio riattivo la lingua della request
        translation.deactivate()
        translation.activate(lang_request)

        return JsonResponse(data)

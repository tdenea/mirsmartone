from builtins import reversed

from django.shortcuts import render
from oscar.views.decorators import permissions_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Q
from datetime import datetime

from notify_user.models import AbandonedCartMailHistory

@permissions_required((['is_staff',], ['partner.dashboard_access']))
def AbandonedCartHistoryView(request):
    searchfield = request.GET.get("searchfield")
    daterange = request.GET.get("daterange")
    dateStart = request.GET.get("start")
    dateEnd = request.GET.get("end")
    sort = request.GET.get("sort")
    dir = request.GET.get("dir")
    status = request.GET.get("status")
    d = {}

    if searchfield or daterange or sort or status:
        abandonedCartData = AbandonedCartMailHistory.objects.all().annotate(num_lines=Count('basket__lines')).order_by("-id")

        # Date range
        if dateStart and dateEnd:
            start = datetime.strptime(str(dateStart), "%Y-%m-%d %H:%M")
            end = datetime.strptime(str(dateEnd), "%Y-%m-%d %H:%M")
            abandonedCartData = abandonedCartData.filter(Q(first_reminder_mail_date__range=[start,end]) | Q(second_reminder_mail_date__range=[start,end]) |
                                                                        Q(third_reminder_mail_date__range=[start,end]))
        # Status
        if status:
            abandonedCartData = abandonedCartData.filter(history_status=status)

        # Search Field
        if searchfield:
            abandonedCartData = abandonedCartData.filter(Q(user__first_name__icontains=searchfield) | Q(user__last_name__icontains=searchfield) | Q(user__email__icontains=searchfield) | Q(basket__lines__product__title__icontains=searchfield) | Q(basket__lines__product__upc__icontains=searchfield)).distinct()

        # Sort
        if sort:
            sortField = ''
            if sort == 'email':
                sortField = 'user__email'
            elif sort == 'first_name':
                sortField = 'user__first_name'
            elif sort == 'last_name':
                sortField = 'user__last_name'
            elif sort == 'lines':
                sortField = 'num_lines'
            elif sort == 'id':
                sortField = 'id'
            elif sort == 'first_reminder':
                sortField = 'first_reminder_mail_date'
            elif sort == 'second_reminder':
                sortField = 'second_reminder_mail_date'
            elif sort == 'third_reminder':
                sortField = 'third_reminder_mail_date'
            elif sort == 'status':
                sortField = 'history_status'
            if sortField and dir == 'desc':
                sortField = '-'+sortField
            if sortField:
                abandonedCartData = abandonedCartData.order_by(sortField)

        d["dir"] = dir if dir else ""
        d["sort"] = sort if sort else ""
        d["searchfield"] = searchfield if searchfield else ""
        d["start"] = dateStart if dateStart else ""
        d["end"] = dateEnd if dateEnd else ""
        d["status"] = status if status else ""
    else:
        abandonedCartData = AbandonedCartMailHistory.objects.all().order_by("-id")
        d["dir"] = ""
        d["sort"] = ""
        d["searchfield"] = ""
        d["start"] = ""
        d["end"] = ""
        d["status"] = ""
    paginator = Paginator(abandonedCartData, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    d["abandonedCartData"] = page_obj
    return render(request,'oscar/dashboard/abandoned-cart-history/index.html',d)


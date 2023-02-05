from django.conf.urls import url
from .views import AbandonedCartHistoryView
from .cron import sent_mail_onclick

urlpatterns = [
    url(r'^abandoned-cart/$',AbandonedCartHistoryView,name='abandoned-history'),
    url(r'^sent_mail/$', sent_mail_onclick, name='sent_mail'),
]

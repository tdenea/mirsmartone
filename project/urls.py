from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.apps import apps
from home import views as home_views
from django.contrib.sitemaps import views
from checkout import custom_paypal
from search import views as search_views
from home.sitemaps import base_sitemaps

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^i18n/', include("django.conf.urls.i18n")),
    url(r'^send_contact/', home_views.save_contact, name='send_contact'),
    url(r'^send_newsletter/', home_views.save_newsletter, name='send_newsletter'),
    url(r'^send_customer_service/', home_views.save_customer_service, name='send_customer_service'),
    url(r'^get_states/', home_views.get_states, name='get_states'),
    url(r'^get_cities/', home_views.get_cities, name='get_cities'),
    url(r'^add_both_one/', home_views.add_both_one, name='add_both_one'),
    url(r'^add_both_oxi/', home_views.add_both_oxi, name='add_both_oxi'),
    url(r'^api/', include("oscarapi.urls")),
    url(r'^sitemap.xml', views.index,
        {'sitemaps': base_sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml', views.sitemap,
        {'sitemaps': base_sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    # url("sitemap.xml", sitemap),
    
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^search/', search_views.search, name='search'),
    # Paypal
    url(
        r"^checkout/paypal/place-order/(?P<basket_id>\d+)/$",
        custom_paypal.SuccessResponseView.as_view(),
        name="paypal-place-order",
    ),
    url(
        r"^checkout/paypal/preview/(?P<basket_id>\d+)/$",
        custom_paypal.SuccessResponseView.as_view(),
        name="paypal-success-response",
    ),
    url(
        r"^checkout/paypal/redirect/",
        custom_paypal.RedirectView.as_view(),
        name="paypal-redirect",
    ),
    url(
        r"^checkout/paypal/payment/",
        custom_paypal.RedirectView.as_view(as_payment_method=True),
        name="paypal-direct-payment",
    ),
    url(r'^checkout/paypal/', include('paypal.express.urls')),

    url(r'^shop/', include(apps.get_app_config('oscar').urls[0])),

    re_path(r'^/$', home_views.slug_view, name='slug-home'),
    re_path(r'(?P<slug>[\w\-]+)/$', home_views.slug_view, name='slug'),

    url(r"^shop/dashboard/", include('notify_user.urls')),

    url("", include(wagtail_urls)),
)
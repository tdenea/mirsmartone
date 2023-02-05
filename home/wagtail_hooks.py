from django.utils.html import format_html
from wagtail.core import hooks
from wagtail.admin.menu import MenuItem
from django.urls import reverse
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ( ModelAdmin, ThumbnailMixin, modeladmin_register)
from wagtailorderable.modeladmin.mixins import OrderableMixin
from home.models import *


@hooks.register("insert_global_admin_js", order=100)
def global_admin_js():
    """Add /static/css/custom.js to the admin."""
    return format_html(
        '<script src="{}?v=1.0"></script>\n',
        static("/js/customadmin.js")
    )

class FormContactAdmin(ModelAdmin):
	model = FormContact
	search_fields = ('name', 'email', 'message',)
	list_display = ('name', 'phone', 'email', 'message', 'date_received', 'privacy', 'newsletter',)
	menu_label = 'Contacts'
	menu_icon = 'form'

class FormNewsletterAdmin(ModelAdmin):
    model = FormNewsletter
    list_display = ('email', 'date_subscribe')
    search_fields = ('email', 'date_subscribe')
    menu_label = 'Form Newsletter'
    menu_icon = 'mail'
    list_per_page = 40
    
class FormCustomerServiceAdmin(ModelAdmin):
	model = FormCustomerService
	search_fields = ('name', 'surname', 'email', 'message',)
	list_display = ('name', 'surname', 'phone', 'email', 'message', 'date_received', 'privacy',)
	menu_label = 'Customer Service'
	menu_icon = 'form'

# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(FormContactAdmin)
modeladmin_register(FormCustomerServiceAdmin)

@hooks.register("register_admin_menu_item")
def register_admin_menu_item():
    return MenuItem(
        _("Shop Dashboard"),
        reverse("dashboard:index"),
        classnames="icon icon-site",
        order=9999,
    )

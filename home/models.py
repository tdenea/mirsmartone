from tabnanny import verbose
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from django.utils import translation
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, FieldRowPanel, MultiFieldPanel, InlinePanel, TabbedInterface, ObjectList, PageChooserPanel
from .translation import TranslatedField
from django_countries.fields import CountryField
from home.base_blocks import *

class HomePage(Page):
    max_count = 1

    # Fields
    title_it = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Title'))
    title_de = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Title'))
    title_fr = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Title'))
    title_es = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Title'))

    translated_title = TranslatedField(
                        'title',
                        'title_it',
                        'title_de',
                        'title_fr',
                        'title_es',
                        )


    # Promote fields
    slug_it = models.SlugField(max_length=255)
    slug_de = models.SlugField(max_length=255)
    slug_fr = models.SlugField(max_length=255)
    slug_es = models.SlugField(max_length=255)

    seo_title_it = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Title tag it'))
    seo_title_de = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Title tag de'))
    seo_title_fr = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Title tag fr'))
    seo_title_es = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Title tag es'))

    search_description_it = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Meta description it'))
    search_description_de = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Meta description de'))
    search_description_fr = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Meta description fr'))
    search_description_es = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Meta description es'))

    translated_slug = TranslatedField(
                    'slug',
                    'slug_it',
                    'slug_de',
                    'slug_fr',
                    'slug_es',
                    )

    translated_seo_title = TranslatedField(
                        'seo_title',
                        'seo_title_it',
                        'seo_title_de',
                        'seo_title_fr',
                        'seo_title_es',
                        )

    translated_search_description = TranslatedField(
                        'search_description',
                        'search_description_it',
                        'search_description_de',
                        'search_description_fr',
                        'search_description_es',
                        )

    # Panels
    content_panels = Page.content_panels + [
    ]

    italian_content_panel = [
        FieldPanel('title_it', classname='full'),
    ]

    german_content_panel = [
        FieldPanel('title_de', classname='full'),
    ]

    french_content_panel = [
        FieldPanel('title_fr', classname='full'),
    ]

    spanish_content_panel = [
        FieldPanel('title_es', classname='full'),
    ]

    promote_panels = [
        MultiFieldPanel(
            [
                FieldPanel('slug', classname="col-6"),
                FieldPanel('slug_it', classname="col-6"),
                FieldPanel('slug_de', classname="col-6"),
                FieldPanel('slug_fr', classname="col-6"),
                FieldPanel('slug_es', classname="col-6"),
            ],
            heading='Slug', 
            classname='collapsible'
        ),
        MultiFieldPanel(
            [
                FieldPanel('seo_title', classname="col-6"),
                FieldPanel('seo_title_it', classname="col-6"),
                FieldPanel('seo_title_de', classname="col-6"),
                FieldPanel('seo_title_fr', classname="col-6"),
                FieldPanel('seo_title_es', classname="col-6"),
            ],
            heading='Titolo Seo', 
            classname='collapsible'
        ),
        MultiFieldPanel(
            [
                FieldPanel('search_description'),
                FieldPanel('search_description_it'),
                FieldPanel('search_description_de'),
                FieldPanel('search_description_fr'),
                FieldPanel('search_description_es'),
            ],
            heading='Meta description', 
            classname='collapsible'
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='en'),
        ObjectList(italian_content_panel, heading='it'),
        ObjectList(german_content_panel, heading='de'),
        ObjectList(french_content_panel, heading='fr'),
        ObjectList(spanish_content_panel, heading='es'),
        ObjectList(promote_panels, heading=_('Promote')),
        ObjectList(Page.settings_panels, heading=_('Settings'), classname="settings")
    ])

    def get_absolute_url(self):
        return '/' + translation.get_language() + '/'
    
    def get_template(self, request):
        return "index.html"
    
    preview_modes = [
        ('form', _('Preview')),
        ('lang_it', _('Preview in Italian')),
        ('lang_de', _('Preview in German')),
        ('lang_fr', _('Preview in French')),
        ('lang_es', _('Preview in Spanish')),
    ]

    def serve_preview(self, request, mode_name):
        if mode_name == 'lang_it':
            request.is_preview = True
            translation.activate('it')
            request.session[translation.LANGUAGE_SESSION_KEY] = 'it'
            return super().serve_preview(request, mode_name)
        elif mode_name == 'lang_de':
            request.is_preview = True
            translation.activate('de')
            request.session[translation.LANGUAGE_SESSION_KEY] = 'de'
            return super().serve_preview(request, mode_name)
        elif mode_name == 'lang_fr':
            request.is_preview = True
            translation.activate('fr')
            request.session[translation.LANGUAGE_SESSION_KEY] = 'fr'
            return super().serve_preview(request, mode_name)
        elif mode_name == 'lang_es':
            request.is_preview = True
            translation.activate('es')
            request.session[translation.LANGUAGE_SESSION_KEY] = 'es'
            return super().serve_preview(request, mode_name)
        else:
            translation.activate('en')
            request.session[translation.LANGUAGE_SESSION_KEY] = 'en'
            return super().serve_preview(request, mode_name)
    
    class Meta:
        verbose_name = "Homepage"
    subpage_types = [
        'home.BasePage',
        'home.TextualPage',
    ]


class BasePage(Page):

    # Fields
    title_it = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Title'))
    title_de = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Title'))
    title_fr = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Title'))
    title_es = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Title'))

    translated_title = TranslatedField(
                        'title',
                        'title_it',
                        'title_de',
                        'title_fr',
                        'title_es',
                        )


    # Promote fields
    slug_it = models.SlugField(max_length=255)
    slug_de = models.SlugField(max_length=255)
    slug_fr = models.SlugField(max_length=255)
    slug_es = models.SlugField(max_length=255)

    seo_title_it = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Title tag it'))
    seo_title_de = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Title tag de'))
    seo_title_fr = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Title tag fr'))
    seo_title_es = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Title tag es'))

    search_description_it = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Meta description it'))
    search_description_de = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Meta description de'))
    search_description_fr = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Meta description fr'))
    search_description_es = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Meta description es'))

    translated_slug = TranslatedField(
                    'slug',
                    'slug_it',
                    'slug_de',
                    'slug_fr',
                    'slug_es',
                    )

    translated_seo_title = TranslatedField(
                        'seo_title',
                        'seo_title_it',
                        'seo_title_de',
                        'seo_title_fr',
                        'seo_title_es',
                        )

    translated_search_description = TranslatedField(
                        'search_description',
                        'search_description_it',
                        'search_description_de',
                        'search_description_fr',
                        'search_description_es',
                        )

    # Panels
    content_panels = Page.content_panels + [
    ]

    italian_content_panel = [
        FieldPanel('title_it', classname='full'),
    ]

    german_content_panel = [
        FieldPanel('title_de', classname='full'),
    ]

    french_content_panel = [
        FieldPanel('title_fr', classname='full'),
    ]

    spanish_content_panel = [
        FieldPanel('title_es', classname='full'),
    ]

    promote_panels = [
        MultiFieldPanel(
            [
                FieldPanel('slug', classname="col-6"),
                FieldPanel('slug_it', classname="col-6"),
                FieldPanel('slug_de', classname="col-6"),
                FieldPanel('slug_fr', classname="col-6"),
                FieldPanel('slug_es', classname="col-6"),
            ],
            heading='Slug', 
            classname='collapsible'
        ),
        MultiFieldPanel(
            [
                FieldPanel('seo_title', classname="col-6"),
                FieldPanel('seo_title_it', classname="col-6"),
                FieldPanel('seo_title_de', classname="col-6"),
                FieldPanel('seo_title_fr', classname="col-6"),
                FieldPanel('seo_title_es', classname="col-6"),
            ],
            heading='Titolo Seo', 
            classname='collapsible'
        ),
        MultiFieldPanel(
            [
                FieldPanel('search_description'),
                FieldPanel('search_description_it'),
                FieldPanel('search_description_de'),
                FieldPanel('search_description_fr'),
                FieldPanel('search_description_es'),
            ],
            heading='Meta description', 
            classname='collapsible'
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='en'),
        ObjectList(italian_content_panel, heading='it'),
        ObjectList(german_content_panel, heading='de'),
        ObjectList(french_content_panel, heading='fr'),
        ObjectList(spanish_content_panel, heading='es'),
        ObjectList(promote_panels, heading=_('Promote')),
        ObjectList(Page.settings_panels, heading=_('Settings'), classname="settings")
    ])

    def get_absolute_url(self):
        return '/' + translation.get_language() + '/' + self.translated_slug + '/'
    
    def get_template(self, request):
        return self.slug + '.html'
    
    preview_modes = [
        ('form', _('Preview')),
        ('lang_it', _('Preview in Italian')),
        ('lang_de', _('Preview in German')),
        ('lang_fr', _('Preview in French')),
        ('lang_es', _('Preview in Spanish')),
    ]

    def serve_preview(self, request, mode_name):
        if mode_name == 'lang_it':
            request.is_preview = True
            translation.activate('it')
            request.session[translation.LANGUAGE_SESSION_KEY] = 'it'
            return super().serve_preview(request, mode_name)
        elif mode_name == 'lang_de':
            request.is_preview = True
            translation.activate('de')
            request.session[translation.LANGUAGE_SESSION_KEY] = 'de'
            return super().serve_preview(request, mode_name)
        elif mode_name == 'lang_fr':
            request.is_preview = True
            translation.activate('fr')
            request.session[translation.LANGUAGE_SESSION_KEY] = 'fr'
            return super().serve_preview(request, mode_name)
        elif mode_name == 'lang_es':
            request.is_preview = True
            translation.activate('es')
            request.session[translation.LANGUAGE_SESSION_KEY] = 'es'
            return super().serve_preview(request, mode_name)
        else:
            translation.activate('en')
            request.session[translation.LANGUAGE_SESSION_KEY] = 'en'
            return super().serve_preview(request, mode_name)
    
    class Meta:
        verbose_name = "Base Page"

class TextualPage(Page):

    # Fields
    title_it = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Title'))
    title_de = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Title'))
    title_fr = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Title'))
    title_es = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Title'))

    translated_title = TranslatedField(
                        'title',
                        'title_it',
                        'title_de',
                        'title_fr',
                        'title_es',
                        )

    description = RichTextField(blank=True, null=True, verbose_name=_('Description'))
    description_it = RichTextField(blank=True, null=True, verbose_name=_('Description'))
    description_de = RichTextField(blank=True, null=True, verbose_name=_('Description'))
    description_fr = RichTextField(blank=True, null=True, verbose_name=_('Description'))
    description_es = RichTextField(blank=True, null=True, verbose_name=_('Description'))

    translated_description = TranslatedField(
        'description',
        'description_it',
        'description_de',
        'description_fr',
        'description_es',
    )

    # Promote fields
    slug_it = models.SlugField(max_length=255)
    slug_de = models.SlugField(max_length=255)
    slug_fr = models.SlugField(max_length=255)
    slug_es = models.SlugField(max_length=255)

    seo_title_it = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Title tag it'))
    seo_title_de = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Title tag de'))
    seo_title_fr = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Title tag fr'))
    seo_title_es = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Title tag es'))

    search_description_it = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Meta description it'))
    search_description_de = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Meta description de'))
    search_description_fr = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Meta description fr'))
    search_description_es = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Meta description es'))

    translated_slug = TranslatedField(
                    'slug',
                    'slug_it',
                    'slug_de',
                    'slug_fr',
                    'slug_es',
                    )

    translated_seo_title = TranslatedField(
                        'seo_title',
                        'seo_title_it',
                        'seo_title_de',
                        'seo_title_fr',
                        'seo_title_es',
                        )

    translated_search_description = TranslatedField(
                        'search_description',
                        'search_description_it',
                        'search_description_de',
                        'search_description_fr',
                        'search_description_es',
                        )

    # Panels
    content_panels = Page.content_panels + [
        FieldPanel('description'),
    ]

    italian_content_panel = [
        FieldPanel('title_it', classname='full'),
        FieldPanel('description_it'),
    ]

    german_content_panel = [
        FieldPanel('title_de', classname='full'),
        FieldPanel('description_de'),
    ]

    french_content_panel = [
        FieldPanel('title_fr', classname='full'),
        FieldPanel('description_fr'),
    ]

    spanish_content_panel = [
        FieldPanel('title_es', classname='full'),
        FieldPanel('description_es'),
    ]

    promote_panels = [
        MultiFieldPanel(
            [
                FieldPanel('slug', classname="col-6"),
                FieldPanel('slug_it', classname="col-6"),
                FieldPanel('slug_de', classname="col-6"),
                FieldPanel('slug_fr', classname="col-6"),
                FieldPanel('slug_es', classname="col-6"),
            ],
            heading='Slug', 
            classname='collapsible'
        ),
        MultiFieldPanel(
            [
                FieldPanel('seo_title', classname="col-6"),
                FieldPanel('seo_title_it', classname="col-6"),
                FieldPanel('seo_title_de', classname="col-6"),
                FieldPanel('seo_title_fr', classname="col-6"),
                FieldPanel('seo_title_es', classname="col-6"),
            ],
            heading='Titolo Seo', 
            classname='collapsible'
        ),
        MultiFieldPanel(
            [
                FieldPanel('search_description'),
                FieldPanel('search_description_it'),
                FieldPanel('search_description_de'),
                FieldPanel('search_description_fr'),
                FieldPanel('search_description_es'),
            ],
            heading='Meta description', 
            classname='collapsible'
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='en'),
        ObjectList(italian_content_panel, heading='it'),
        ObjectList(german_content_panel, heading='de'),
        ObjectList(french_content_panel, heading='fr'),
        ObjectList(spanish_content_panel, heading='es'),
        ObjectList(promote_panels, heading=_('Promote')),
        ObjectList(Page.settings_panels, heading=_('Settings'), classname="settings")
    ])

    def get_absolute_url(self):
        return '/' + translation.get_language() + '/' + self.translated_slug + '/'
    
    def get_template(self, request):
        return 'textual-page.html'
    
    preview_modes = [
        ('form', _('Preview')),
        ('lang_it', _('Preview in Italian')),
        ('lang_de', _('Preview in German')),
        ('lang_fr', _('Preview in French')),
        ('lang_es', _('Preview in Spanish')),
    ]

    def serve_preview(self, request, mode_name):
        if mode_name == 'lang_it':
            request.is_preview = True
            translation.activate('it')
            request.session[translation.LANGUAGE_SESSION_KEY] = 'it'
            return super().serve_preview(request, mode_name)
        elif mode_name == 'lang_de':
            request.is_preview = True
            translation.activate('de')
            request.session[translation.LANGUAGE_SESSION_KEY] = 'de'
            return super().serve_preview(request, mode_name)
        elif mode_name == 'lang_fr':
            request.is_preview = True
            translation.activate('fr')
            request.session[translation.LANGUAGE_SESSION_KEY] = 'fr'
            return super().serve_preview(request, mode_name)
        elif mode_name == 'lang_es':
            request.is_preview = True
            translation.activate('es')
            request.session[translation.LANGUAGE_SESSION_KEY] = 'es'
            return super().serve_preview(request, mode_name)
        else:
            translation.activate('en')
            request.session[translation.LANGUAGE_SESSION_KEY] = 'en'
            return super().serve_preview(request, mode_name)
    
    class Meta:
        verbose_name = "Textual Page"

class FormContact(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Fullname"))
    phone = models.CharField(max_length=100, verbose_name=_("Phone number"))
    email = models.EmailField()
    message = models.TextField(verbose_name='Message')
    privacy = models.BooleanField(default=False, verbose_name=_("Privacy"))
    newsletter = models.BooleanField(default=False, verbose_name=_("Newsletter"))
    date_received = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Data"))
    
    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('surname'),
            FieldPanel('phone'),
            FieldPanel('email'),
        ],
        classname="collapsible"),
        FieldPanel('message'),
    ]

    class Meta:
        verbose_name = _("Form Contact")
        verbose_name_plural = _("Form Contacts")

class FormNewsletter(models.Model):
    email = models.EmailField()
    privacy = models.BooleanField(default=False)
    date_subscribe = models.DateTimeField(auto_now_add=True, null=True)

    panels = [
        FieldPanel("email"),
    ]

    class Meta:
        verbose_name = _("Form Newsletter")
        verbose_name_plural = _("Form Newsletters")
        
class FormCustomerService(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("First Name"))
    surname = models.CharField(max_length=200, verbose_name=_("Last Name"))
    phone = models.CharField(max_length=100, verbose_name=_("Phone number"))
    email = models.EmailField()
    message = models.TextField(verbose_name='Message')
    privacy = models.BooleanField(default=False, verbose_name=_("Privacy"))
    date_received = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Data"))
    
    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('surname'),
            FieldPanel('phone'),
            FieldPanel('email'),
        ],
        classname="collapsible"),
        FieldPanel('message'),
    ]

    class Meta:
        verbose_name = _("Form Customer Service")
        verbose_name_plural = _("Form Customer Service")

@register_setting
class SiteSettings(BaseSetting):
    name = models.CharField(max_length=200, default="MIR", verbose_name=_("Name"))
    google_analytics_id = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Google Analytics ID"))
    google_analytics_test = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Google Analytics TEST ID"))
    addresses = StreamField([
            ('address', AddressBlock()),
        ], null=True, blank=True)
    mymir_registration = models.URLField(null=True, blank=True, help_text='MyMir Registration URL')
    mymir_login = models.URLField(null=True, blank=True, help_text='MyMir Login URL')
    instagram = models.URLField(null=True, blank=True, help_text='Instagram URL')
    facebook = models.URLField(null=True, blank=True, help_text='Facebook URL')
    twitter = models.URLField(null=True, blank=True, help_text='Twitter URL')
    youtube = models.URLField(null=True, blank=True, help_text='Youtube URL')
    linkedin = models.URLField(null=True, blank=True, help_text='Linkedin URL')

    panels = [
        FieldPanel('name',),
        FieldPanel('google_analytics_id',),
        FieldPanel('google_analytics_test',),
        StreamFieldPanel('addresses'),
        FieldPanel('mymir_registration'),
        FieldPanel('mymir_login'),
        FieldPanel('instagram'),
        FieldPanel('facebook'),
        FieldPanel('twitter'),
        FieldPanel('youtube'),
        FieldPanel('linkedin'),
    ]
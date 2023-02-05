# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.utils.encoding import force_str
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.core import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.core.blocks import DateBlock, BooleanBlock, IntegerBlock, PageChooserBlock, EmailBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail_color_panel.blocks import NativeColorBlock

ALIGN_OPTIONS = (
    ('center', 'Al centro'),
    ('left', 'A sinistra'),
    ('right', 'A destra'),
)

class FormBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label='Title Button',)
    form_open = blocks.BooleanBlock(required=False, help_text='Check se il form inizializza aperto')

# Title, description and image
class SingleTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label=_('Title'))
    description = blocks.TextBlock(required=False, label='Description',)
    svg = blocks.TextBlock(required=False)
    image = ImageChooserBlock(required=False, label=_('Image'),)
    immagine_a_destra = blocks.BooleanBlock(required=False, help_text='Check se immagine va a destra del testo')

class CitBlock(blocks.StructBlock):
    description = blocks.TextBlock(label='Citazione',)
    name = blocks.CharBlock(required=False, label='Nome/Fonte')

    class Meta:
        label = 'Citazione'
        icon = 'openquote'

class CitazioniBlock(blocks.StructBlock):
    lista = blocks.ListBlock(CitBlock())

    class Meta:
        icon = 'openquote'


# Single block icon title description
class SingleItemsBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)
    description = blocks.RichTextBlock(required=False, null=True, blank=True, label='Description',)
    svg = blocks.TextBlock(required=False)

class TimelineItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)
    description = blocks.RichTextBlock(required=False, null=True, blank=True, label='Description',)
    svg = blocks.TextBlock(required=False)
    image = ImageChooserBlock(required=False, null=True, blank=True, label=_('Image'))

    class Meta:
        icon = 'date'

# Title, description, blocks - icon / title / description
class TitleDescBlocchiBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label=_('Title'))
    description = blocks.RichTextBlock(required=False, null=True, blank=True, label='Description',)
    lista = blocks.ListBlock(SingleItemsBlock())
    icona_blocchi = blocks.BooleanBlock(required=False, help_text="Check se c'è icona")

    class Meta:
        icon = 'doc-full'

# Number block
class NumberItemBlock(blocks.StructBlock):
    number = blocks.IntegerBlock(required=False, null=True, blank=True, label='Number')
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)
    description = blocks.RichTextBlock(required=False, null=True, blank=True, label='Description',)

# Title, description, blocks - icon / title / description
class NumbersBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label=_('Title'))
    description = blocks.RichTextBlock(required=False, null=True, blank=True, label='Description',)
    lista = blocks.ListBlock(NumberItemBlock())

    class Meta:
        icon = 'doc-full'

# Solo testo
class OnlyTextBlock(blocks.StructBlock):
    description = blocks.RichTextBlock(required=False, null=True, blank=True, label='Description',)

    class Meta:
        icon = 'pilcrow'

# Solo email
class OnlyEmailBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)
    email = blocks.EmailBlock(required=False, null=True, blank=True,)

    class Meta:
        icon = 'mail'

# Telefoni
class TelBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)
    number = blocks.CharBlock(required=False, null=True, blank=True, label='Number',)

    class Meta:
        icon = 'mail'

# Solo title
class OnlyTitleBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)

    class Meta:
        icon = 'pilcrow'

class TitleBtnBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label='Title Button',)

    class Meta:
        icon = 'tag'

class DomandaBlock(blocks.StructBlock):
    domanda = blocks.RichTextBlock(required=False, null=True, blank=True,)

    class Meta:
        icon = 'pilcrow'

# Title, description and button
class TextDescDocBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label=_('Title'))
    description = blocks.RichTextBlock(required=False, null=True, blank=True, label='Description',)
    title_btn = blocks.CharBlock(required=False, label='Title button')
    document = DocumentChooserBlock(required=False, label=_('Upload a document'))
    link_external = blocks.URLBlock(required=False, null=True, blank=True, label='External Link')
    mailchimp_form = blocks.TextBlock(required=False, null=True, blank=True,)
    domande = blocks.ListBlock(DomandaBlock())

    class Meta:
        icon = 'doc-full'

# Title, link and doc
class TitleLinkDocBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label=_('Title'))
    document = DocumentChooserBlock(required=False, label=_('Upload a document'))
    link_external = blocks.URLBlock(required=False, null=True, blank=True, label='External Link')

    class Meta:
        icon = 'doc-full'

# Title and list
class ListBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label=_('Title'))
    lista = blocks.ListBlock(OnlyTextBlock())
    
    class Meta:
        icon = 'list-ol'

# Solo Video
class SingleVideoBlock(blocks.StructBlock):
    video_url = blocks.CharBlock(label='Youtube URL video', required=False, null=True, blank=True, help_text='URL con embed, ex: https://www.youtube.com/embed/XxXxXxXxXx')

    class Meta:
        icon = 'media'

# Solo Video
class VideoEmbedBlock(blocks.StructBlock):
    video = EmbedBlock(label='URL video', required=False, null=True, blank=True)

    class Meta:
        icon = 'media'

# Solo Immagine
class SingleImageBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)
    image = ImageChooserBlock(required=False, null=True, blank=True, label=_('Image'))
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Link to page')
    link_external = blocks.URLBlock(required=False, null=True, blank=True, label='External Link')

    class Meta:
        icon = 'image'

class OnlyImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False, null=True, blank=True, label=_('Image'))

    class Meta:
        icon = 'image'

# Logo block
class LogoSingleBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)
    image = ImageChooserBlock(required=False, null=True, blank=True, label=_('Image'))
    link_external = blocks.URLBlock(required=False, null=True, blank=True, label='External Link')

    class Meta:
        icon = 'image'

# Immagine più testo
class ImageTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)
    description = blocks.RichTextBlock(required=False, null=True, blank=True, label='Description')
    image = ImageChooserBlock(required=False, null=True, blank=True, label=_('Image'))
    immagine_a_destra = blocks.BooleanBlock(required=False, null=True, blank=True, help_text='Check se immagine/documento va a destra del testo')
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Link to page')

    class Meta:
        icon = 'doc-full-inverse'

# Slider multiple images
class SliderBlock(blocks.StructBlock):
    carousel = blocks.ListBlock(SingleImageBlock())

    class Meta:
        icon = 'image'

class TitleImageBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)
    image = ImageChooserBlock(required=False, null=True, blank=True, label=_('Image'))

    class Meta:
        icon = 'image'

# Slider multiple images
class SliderImageBlock(blocks.StructBlock):
    carousel = blocks.ListBlock(TitleImageBlock())

    class Meta:
        icon = 'image'

# Single logo
class LogoImageBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)
    image = ImageChooserBlock(required=False, null=True, blank=True, label=_('Image'))
    link = blocks.CharBlock(required=False, null=True, blank=True)

    class Meta:
        icon = 'image'

# Logo's block
class LogoBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)
    description = blocks.RichTextBlock(required=False, null=True, blank=True, label='Description')
    loghi = blocks.ListBlock(LogoImageBlock())

    class Meta:
        icon = 'image'

class MiniTestimonialBlock(blocks.StructBlock):
    testo = blocks.RichTextBlock(required=False, null=True, blank=True,)
    nome = blocks.CharBlock(required=False)

    class Meta:
        icon = 'openquote'

class CaseSingleBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)
    description = blocks.RichTextBlock(required=False, null=True, blank=True, label='Description')
    image = ImageChooserBlock(required=False, null=True, blank=True, label=_('Image'))

    class Meta:
        icon = 'doc-full-inverse'

class LavoraConNoiBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)
    description = blocks.RichTextBlock(required=False, null=True, blank=True, label='Description')

    class Meta:
        icon = 'doc-full-inverse'

class SingleLinkBlock(blocks.StructBlock):
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Link to page')

    class Meta:
        icon = 'link'

class NewsRelatedBlock(blocks.StructBlock):
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Link to page', page_type='news.NewsPage')

    class Meta:
        icon = 'doc-full'

class OnlyPhoneBlock(blocks.StructBlock):
    tel = blocks.CharBlock(label='Telefono',)
    class Meta:
        label='Telefono'

class OnlyEmailBlock(blocks.StructBlock):
    email = EmailBlock(label='Email',)

class OnlyWebsitesBlock(blocks.StructBlock):
    website = blocks.URLBlock(label='Website')

class AccordionItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'))
    description = blocks.RichTextBlock(label='Description',)

    class Meta:
        icon = 'pilcrow'

class AccordionBlock(blocks.StructBlock):
    accordion_list = blocks.ListBlock(AccordionItemBlock())

    class Meta:
        icon = 'list-ul'

class OnlyDocBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label=_('Title'))
    document = DocumentChooserBlock(required=False, label=_('Upload a document'))

    class Meta:
        icon = 'doc-full'
        
class TitleTextImageBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'))
    description = blocks.RichTextBlock(label='Description',)
    image = ImageChooserBlock(label=_('Image'),)

new_table_options = {
    'minSpareRows': 0,
    'startRows': 3,
    'startCols': 3,
    'colHeaders': False,
    'rowHeaders': False,
    'contextMenu': [
        'row_above',
        'row_below',
        '---------',
        'col_left',
        'col_right',
        '---------',
        'remove_row',
        'remove_col',
        '---------',
        'undo',
        'redo',
        '---------',
        'copy',
        'cut',
        '---------',
        'alignment',
    ],
    'editor': 'text',
    'stretchH': 'all',
    'renderer': 'text',
    'autoColumnSize': False,
    'language': 'en-US',
}

class CustomTableBlock(blocks.StructBlock):
    table = TableBlock(label='Tabella HTML', table_options=new_table_options)

    class Meta:
        icon = 'table'

class HeroBlock(blocks.StructBlock):
    title = blocks.TextBlock(label=_('Title'),)
    image = ImageChooserBlock(label=_('Image'),)
    title_btn = blocks.CharBlock(required=False, label='Title button')
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Link to page')

    class Meta:
        icon = 'pick'

class GuideSectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'))
    description = blocks.RichTextBlock(label='Description',)

    class Meta:
        label = 'Sezione Guida Tecnologica'

# Number block
class SimpleNumberBlock(blocks.StructBlock):
    number = blocks.CharBlock(required=False, null=True, blank=True, label='Number')
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)

class BoxImageTextQuoteBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'))
    description = blocks.RichTextBlock(label='Description',)
    numbers = blocks.ListBlock(SimpleNumberBlock())
    quote = blocks.CharBlock(required=False, null=True, blank=True, label='Citazione',)
    quote_source = blocks.CharBlock(required=False, null=True, blank=True, label='Fonte citazione',)
    image = ImageChooserBlock(label=_('Image'),)

    class Meta:
        label = 'Title, testo, numeri, citazione e immagine'
        icon = 'image'

class NewsletterSectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'))
    
    class Meta:
        label = 'Sezione Newsletter'
        icon = 'mail'

class SimpleBoxItemBlock(blocks.StructBlock):
    image = ImageChooserBlock(label=_('Image'),)
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Link to page')
    link_external = blocks.URLBlock(required=False, null=True, blank=True, label='External Link')

class BoxesItemsBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'))
    boxes = blocks.ListBlock(SimpleBoxItemBlock())

class BoxImageColorBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'))
    description = blocks.RichTextBlock(label='Description',)
    title_btn = blocks.CharBlock(required=False, label='Title button')
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Link to page')
    image = ImageChooserBlock(label=_('Image'),)
    color = NativeColorBlock(label='Color', default="#000000")

    class Meta:
        icon = 'image'

class NewsSectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'))

    class Meta:
        label = 'Sezione News'

class TitleCenterBlock(blocks.StructBlock):
    title = blocks.TextBlock(label=_('Title'))

    class Meta:
        label = 'Title'
        icon = 'title'

class DescriptionCenterBlock(blocks.StructBlock):
    description = blocks.RichTextBlock(label='Description')

    class Meta:
        label = 'Description'
        icon = 'pilcrow'

class ValueItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label='Valore Titolo',)

    class Meta:
        icon = 'pilcrow'

class BoxImageBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'))
    description = blocks.RichTextBlock(label='Description',)
    value_title = blocks.CharBlock(required=False, null=True, blank=True, label='Title Valori')
    value_items = blocks.ListBlock(ValueItemBlock())
    image = ImageChooserBlock(label=_('Image'),)

    class Meta:
        label = 'Title, Testo, Valori e Immagine'
        icon = 'image'

class TitleDescBtnImageVideoBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'))
    description = blocks.RichTextBlock(label='Description',)
    title_btn = blocks.CharBlock(label='Title Button',)
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Link to page')
    link_external = blocks.URLBlock(required=False, null=True, blank=True, label='External Link')
    video = EmbedBlock(label='URL video', required=False, null=True, blank=True)
    image = ImageChooserBlock(label=_('Image'), required=False, null=True, blank=True)
    color = NativeColorBlock(label='Color', default="#FDB633")

    class Meta:
        label = 'Title, Testo, Bottone, Immagine o Video'
        icon = 'image'

class InfoSectionColorBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'))
    description = blocks.RichTextBlock(label='Description',)
    title_btn = blocks.CharBlock(label='Title Button',)
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Link to page')
    link_external = blocks.URLBlock(required=False, null=True, blank=True, label='External Link')
    color = NativeColorBlock(label='Color', default="#91A8D0")

class TitleTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'),required=False, null=True, blank=True)
    description = blocks.RichTextBlock(label='Description',required=False, null=True, blank=True)
    position = blocks.CharBlock(label='Allineamento del testo', choices=ALIGN_OPTIONS, default='center')

    class Meta:
        label = 'Title + Testo'
        icon = 'pilcrow'

class HexagonItemsBlock(blocks.StructBlock):
    items = blocks.ListBlock(OnlyTitleBlock())

    class Meta:
        icon = 'grip'
        label = 'Elementi Esagonali'

class ButtonSectionBlock(blocks.StructBlock):
    title_section = blocks.CharBlock(label='Title Sezione',)
    title = blocks.CharBlock(label='Title Button',)
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Link to page')
    link_external = blocks.URLBlock(required=False, null=True, blank=True, label='External Link')
    mailto = blocks.EmailBlock(required=False, null=True, blank=True, label='Link Mail To')

    class Meta:
        label = 'Bottone Section'
        icon = 'link'

class ButtonBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'),)
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Link to page')
    link_external = blocks.URLBlock(required=False, null=True, blank=True, label='External Link')
    mailto = blocks.EmailBlock(required=False, null=True, blank=True, label='Link Mail To')

    class Meta:
        label = 'Bottone Link'
        icon = 'link'

class ButtonDocBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'),)
    document = DocumentChooserBlock(required=False, label=_('Upload a document'))

    class Meta:
        label = 'Bottone Documento'
        icon = 'link'

class BoxPositionHeroBlock(blocks.StructBlock):
    title = blocks.CharBlock(label='Name and Surname',)
    role = blocks.CharBlock(label='Role',)
    company = blocks.CharBlock(label='Company',required=False, null=True, blank=True)
    image = ImageChooserBlock(label='Photo',)

    class Meta:
        icon = 'image'
        label = 'Box Ruolo'


class StaffItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(label='Name and Surname')
    role = blocks.CharBlock(label='Role',)
    image = ImageChooserBlock(label='Photo',)

    class Meta:
        icon = 'pilcrow'

class StaffBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'),)
    staff_list = blocks.ListBlock(StaffItemBlock())

class LogoItemBlock(blocks.StructBlock):
    image = ImageChooserBlock(label='Logo',)
    link_external = blocks.URLBlock(required=False, null=True, blank=True, label='External Link')

class PartnerItemBlock(blocks.StructBlock):
    image = ImageChooserBlock(label='Partner Immagine',)
    link_external = blocks.URLBlock(required=False, null=True, blank=True, label='External Link')

class MembersSectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'),)
    title2 = blocks.CharBlock(label='Title 2',)
    logo_list = blocks.ListBlock(LogoItemBlock())
    partners_list = blocks.ListBlock(PartnerItemBlock())

class ProjectItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'),)
    description = blocks.TextBlock(label='Description',)

class ProjectMasterItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(label='Title Progetto',)
    accordion = blocks.ListBlock(ProjectItemBlock())

class ActiveProjectsBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'),)
    project_list = blocks.ListBlock(ProjectMasterItemBlock())

    class Meta:
        label = 'Progetti Attivi'
        icon = 'pilcrow'

class AnalysisBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'),)
    image_analysis = ImageChooserBlock(required=False, label='Immagine Analisi Master',)
    title_analysis = blocks.CharBlock(label='Title Analisi Master',)
    description_analysis = blocks.RichTextBlock(required=False, null=True, blank=True, label='Descrizione Analisi Master',)
    btn_list = blocks.ListBlock(TitleLinkDocBlock())

    class Meta:
        label = 'Analisi recenti Section'

class EventBlock(blocks.StructBlock):
    title = blocks.CharBlock(label='Title Evento',)
    date_start = blocks.DateBlock(label='Data Inizio Evento')
    date_end = blocks.DateBlock(label='Data Fine Evento')
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Link to page')
    link_external = blocks.URLBlock(required=False, null=True, blank=True, label='External Link')

    class Meta:
        label = 'Evento'

class EventFairBlock(blocks.StructBlock):
    name_line = blocks.CharBlock(required=False, null=True, blank=True, label='Nominativo',)
    address1 = blocks.CharBlock(required=False, null=True, blank=True, label='Indirizzo riga 1',)
    address2 = blocks.CharBlock(required=False, null=True, blank=True, label='Indirizzo riga 2',)
    city = blocks.CharBlock(required=False, null=True, blank=True, label='Città',)
    province = blocks.CharBlock(required=False, null=True, blank=True, label='Provincia',)
    postal_code = blocks.CharBlock(required=False, null=True, blank=True, label='Codice Postale',)
    country = blocks.CharBlock(required=False, null=True, blank=True, label='Paese',)

    class Meta:
        label = 'Fiera'

class CalendarBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'),)

    class Meta:
        label = 'Calendario Section'

class MapBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'),)

    class Meta:
        label = 'Mappa Section'

class SustainabilitySectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'),)
    description = blocks.RichTextBlock(required=False, null=True, blank=True, label='Description',)
    images_list = blocks.ListBlock(OnlyImageBlock())

    class Meta:
        label = 'Sostenibilità Section'

class ImageLinkBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False, null=True, blank=True, label=_('Image'))
    link_external = blocks.URLBlock(required=False, null=True, blank=True, label='External Link')

    class Meta:
        icon = 'image'

class SubMenuBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label='Title Menu')
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Link to page')

    class Meta:
        icon = 'link'

class SingleMenuBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label='Title Menu')
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Pagina')
    childrens = blocks.ListBlock(SubMenuBlock())
    
    class Meta:
        label= 'Menu Item'
        icon = 'link'

class AttachmentBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label=_('Title document'))
    document = DocumentChooserBlock(required=False, label=_('Upload a document'))

    class Meta:
        label='Attachment'
        icon = 'doc-full'

class Attachment2Block(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label=_('Title document'))
    subtitle = blocks.CharBlock(required=False, label=_('Subtitle document'))
    document = DocumentChooserBlock(required=False, label=_('Upload a document'))

    class Meta:
        label='Attachment'
        icon = 'doc-full'

class AttachmentPrivateBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label=_('Title document'))
    document = DocumentChooserBlock(required=False, label=_('Upload a document'))
    private = blocks.BooleanBlock(default=False, null=True, blank=True, required=False, help_text='Check se il documento è visibile soltanto agli utenti con il permesso Utente Consigliere', label='Privato?')

    class Meta:
        label='Allegato'
        icon = 'doc-full'

# Menu Intranet
class SubMenuIntranetBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label='Title Menu')
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Link to page')

    class Meta:
        label= 'Submenu Item'
        icon = 'link'

class SubGroupMenuBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label='Title Gruppo Menu')
    childrens = blocks.ListBlock(SubMenuIntranetBlock())

    class Meta:
        label = 'Gruppo Menu'

class ExternalLinkIntranetBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label='Title Menu')
    link_external = blocks.URLBlock(required=False, null=True, blank=True, label='External Link')
    new_tab = blocks.BooleanBlock(default=True, help_text='Check per aprire il link in una nuova finestra', label='Nuova finestra')

    class Meta:
        label= 'URL esterno'
        icon = 'link'

class SingleMenuIntranetBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label='Title Menu')
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Pagina')
    childrens = blocks.StreamBlock([
        ('subgroup', SubGroupMenuBlock(required=False)),
        ('submenu', SubMenuIntranetBlock(required=False)),
        ('external', ExternalLinkIntranetBlock(required=False)),
    ], null=True, blank=True, required=False)
    
    class Meta:
        label= 'Menu Item'
        icon = 'link'

class TitleSubtitleOnlyBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label=_('Title'))
    subtitle = blocks.CharBlock(required=False, label=_('Subtitle'))

class FeatureBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label=_('Title'))
    subtitle = blocks.TextBlock(required=False, label=_('Subtitle'))
    title_popup = blocks.CharBlock(required=False, label='Title popup')
    description = blocks.RichTextBlock(required=False, null=True, blank=True, label='Description popup',)
    image = ImageChooserBlock(required=False, label=_('Image'),)


class SingleButtonBlock(blocks.StructBlock):
    btn_title = blocks.CharBlock(required=False, null=True, blank=True, label='Title button',)
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Link to page')
    link_external = blocks.URLBlock(required=False, null=True, blank=True, label='External Link')

class EmailBlock(blocks.StructBlock):
    email = blocks.EmailBlock(required=False, null=True, blank=True,)

class PhoneBlock(blocks.StructBlock):
    phone = blocks.CharBlock(required=False, null=True, blank=True,)

class AddressBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label='Title Address',)
    address = blocks.TextBlock(required=False, null=True, blank=True)
    emails = blocks.ListBlock(EmailBlock())
    phones = blocks.ListBlock(PhoneBlock())
    lat = blocks.CharBlock(required=False, null=True, blank=True, label='Latitude',)
    lon = blocks.CharBlock(required=False, null=True, blank=True, label='Longitude',)

class NumberBlock(blocks.StructBlock):
    image = DocumentChooserBlock(required=False, label=_('Icon'))
    number = blocks.IntegerBlock(required=False, null=True, blank=True, label='Number')
    number_symbol = blocks.CharBlock(required=False, null=True, blank=True, label='Number symbol')
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)

class ApproachBlock(blocks.StructBlock):
    image = DocumentChooserBlock(required=False, label=_('Icon'))
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)
    description = blocks.TextBlock(required=False, null=True, blank=True, label=_("Description"))


class BoxCoreBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)
    subtitle = blocks.CharBlock(required=False, null=True, blank=True, label=_('Subtitle'),)
    image = ImageChooserBlock(required=False, label=_('Image'),)
    page_link = PageChooserBlock(required=False, null=True, blank=True, label='Link to page')
    page_link_hash = blocks.CharBlock(required=False, null=True, blank=True, label=_('Hash link'),)


class TestimonialBlock(blocks.StructBlock):
    text = blocks.TextBlock(required=False, null=True, blank=True)
    author = blocks.CharBlock(required=False, null=True, blank=True, label=_('Title'),)
    image = ImageChooserBlock(required=False, label=_('Photo'),)


class SDKBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'),)
    description = blocks.TextBlock(label=_('Description'),)
    image = ImageChooserBlock(label=_('Image'),)
    document = DocumentChooserBlock(required=False, label=_('Brochure file'))
    specs_compatible_spirometer_oximetry = blocks.CharBlock(required=False, null=True, blank=True, label=_('Spec. Compatible Spirometer With Oximetry Option'))
    specs_compatible_spirometer = blocks.CharBlock(required=False, null=True, blank=True, label=_('Spec. Compatible Spirometer (No Oxi)'))
    specs_compatible_os = blocks.CharBlock(required=False, null=True, blank=True, label=_('Spec. Compatible Os'))
    specs_communication = blocks.CharBlock(required=False, null=True, blank=True, label=_('Spec. Communication'))
    specs_programming_language = blocks.CharBlock(required=False, null=True, blank=True, label=_('Spec. Programming Language'))
    specs_compatible_turbine_flowmeter = blocks.CharBlock(required=False, null=True, blank=True, label=_('Spec. Compatible Turbine Flowmeter'))

class BoxContactBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('Title'),)
    subtitle = blocks.CharBlock(label=_('Subtitle'),)

class CertificateBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label=_('Title'))
    document = DocumentChooserBlock(required=False, label=_('Upload a document'))

    class Meta:
        icon = 'doc-full'

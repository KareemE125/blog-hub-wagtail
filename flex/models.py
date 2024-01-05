from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from streams import blocks
# Create your models here.

class FlexPage(Page):

    content = StreamField([ 
            ("title_and_text", blocks.TitleAndTextBlock()), 
            ("cards_list", blocks.CardsBlock()),
        ],use_json_field=True, blank=True, null=True)
    
    subTitle = models.CharField(max_length=100, blank=True, null=True) 
    
    content_panels = Page.content_panels + [
        FieldPanel('subTitle'),
        FieldPanel('content'),
    ]
    

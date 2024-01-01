from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
# Create your models here.

class FlexPage(Page):

    
    subTitle = models.CharField(max_length=100, blank=True, null=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('subTitle'),
    ]
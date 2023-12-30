from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

class HomePage(Page):
    template = "home/home_page.html"
    max_count = 1
    
    description = RichTextField(max_length=255, blank=True)
    image = models.ForeignKey("wagtailimages.Image", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    callToAction = models.ForeignKey("wagtailcore.Page", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    
    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('image'),
        FieldPanel('callToAction'),
    ]
    
    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"

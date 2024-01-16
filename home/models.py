from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.api import APIField


class CarouselImage(Orderable):
    page = ParentalKey("home.HomePage", related_name="carousel_images")
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=False, on_delete=models.SET_NULL, related_name="+")

    panels = [
        FieldPanel("image")
    ]
    
    api_fields = [
        APIField('image'),
    ]


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
        InlinePanel('carousel_images', label="Carousel images", max_num= 5)
    ]
    
    api_fields = [
        APIField('description'),
        APIField('image'),
        APIField('callToAction'),
        APIField('carousel_images'),
    ]
    
    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"

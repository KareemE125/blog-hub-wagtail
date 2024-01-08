from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from streams import blocks

# Create your models here.

class BlogsPage(Page):
    custom_title = models.CharField(max_length=100, blank=False, null=False, help_text='Custom title for the blog detail page')

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
    ]
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["blogs"] = BlogDetailPage.objects.live().public()
        
        return context


class BlogDetailPage(Page):
    
    custom_title = models.CharField(max_length=100, blank=False, null=False, help_text='Custom title for the blog detail page')
    
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    
    content = StreamField([ 
            ("title_and_text", blocks.TitleAndTextBlock()), 
            ("rich_paragraph", blocks.RichtextBlock()),
    ],use_json_field=True, blank=True, null=True)
    
    
    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        FieldPanel('image'),
        FieldPanel('content'),
    ]
    
    
    
    
    
    
    
    
    
    
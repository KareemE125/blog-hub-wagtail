from django.db import models
from django_extensions.db.fields import AutoSlugField

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.models import Page, Orderable 
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet

# Create your models here.
class MenuItem(Orderable):
    page = ParentalKey("Menu", on_delete=models.CASCADE, related_name="menu_items")
    
    link_title = models.CharField(max_length=120, null=True, blank=True)
    link_url = models.CharField(max_length=600, null=True, blank=True)
    link_page = models.ForeignKey("wagtailcore.Page", on_delete=models.CASCADE, null=True, blank=True, related_name="+")
    open_in_new_tab = models.BooleanField(default=True)
    
    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        FieldPanel("link_page"),
        FieldPanel("open_in_new_tab"),
    ]
    
    def save(self, *args, **kwargs):
        link = self.link()
        if not self.link_title: 
            if isinstance(link, Page):
                self.link_title = self.link_page.title
            else:
                self.link_title = link
        super().save(*args, **kwargs) 
        
    def link(self):
        if self.link_url:
            link = self.link_url
        elif self.link_page:
            link = self.link_page
        else:
            link = "/"
    
        return link
    

    
@register_snippet
class Menu(ClusterableModel):
    title = models.CharField(max_length=120)
    slug = AutoSlugField(populate_from='title', editable=True)
    
    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        InlinePanel("menu_items", label="Menu Items")
    ]
    
    def __str__(self):
        return self.title
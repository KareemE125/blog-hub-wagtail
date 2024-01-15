from django.db import models
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from django_extensions.db.fields import AutoSlugField
from urllib.parse import urlparse

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
        
    @property
    def link(self):
        if self.link_url:
            link = self.link_url
        elif self.link_page:
            link = self.link_page.url
        else:
            link = "#"
    
        return link
    
    @property
    def title(self):
        if not self.link_title:
            if self.link_url: 
                domain = urlparse(self.link_url).netloc
                title = domain if domain else self.link_url
            elif self.link_page:
                title = self.link_page.title
            else:
                title = "Visit Site"
        else:
            title = self.link_title
        
        self.link_title = title
        self.save()
        return self.link_title
    

    
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
    
    def save(self, *args, **kwargs):
        cacheKey = make_template_fragment_key(
            "navbar_hanging_preview",
        )
        cache.delete(cacheKey)
        return super().save(*args, **kwargs)
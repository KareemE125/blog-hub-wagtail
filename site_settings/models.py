from django.db import models
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
# Create your models here.

@register_setting
class SocialMediaSettings(BaseSiteSetting):
    
    facebook = models.URLField(null=True, blank=True, help_text="Facebook Link")
    linkedin = models.URLField(null=True, blank=True, help_text="LinkedIn Link")
    youtube = models.URLField(null=True, blank=True, help_text="Youtube Link")

    panels = [
        MultiFieldPanel([
            FieldPanel('facebook'),
            FieldPanel('linkedin'),
            FieldPanel('youtube'),    
        ], heading="Social Media Settings"),
    ]
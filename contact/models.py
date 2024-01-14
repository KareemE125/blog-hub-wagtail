from django.db import models

from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.fields import RichTextField
from modelcluster.fields import ParentalKey

# Create your models here.
class FormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )
    
    
class ContactPage(AbstractEmailForm):
    template = "contact/contact_page.html"
    landing_page_template = "contact/contact_page_landing.html"

    max_count = 1
    
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    class Meta:
        verbose_name = "Contact Page"
        verbose_name_plural = "Contact Pages"
        
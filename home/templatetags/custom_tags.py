# myapp/templatetags/custom_tags.py
from django import template
from wagtail.models import Page
register = template.Library()

@register.inclusion_tag('navbar.html', takes_context=True)
def render_navbar(context):
    request = context['request']
    pages = Page.objects.live().public().exclude(depth=1)
    
    return {'pages': pages, "current_path": request.path }

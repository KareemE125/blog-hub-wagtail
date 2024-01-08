from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, path, re_path

from streams import blocks

# Create your models here.

class BlogsPage(RoutablePageMixin, Page):
    custom_title = models.CharField(max_length=100, blank=False, null=False, help_text='Custom title for the blog detail page')

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
    ]
    
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["blogs"] = BlogDetailPage.objects.live().public().order_by('-last_published_at')
        
        return context
    
    
    @path('latest/<int:num>/', name='latest_blogs')
    @path('latest/', name='latest_blogs')
    def latest_blogs(self, request, num=1):
        self.custom_title = "Latest Blogs"
        
        return self.render(
            request,
            template="blog/latest_blogs.html",
            context_overrides={
                "blogs": self.get_context(request)["blogs"][:num],
            },
        )


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
    
    
    
    
    
    
    
    
    
    
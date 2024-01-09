from django.db import models
from django import forms

from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.snippets.models import register_snippet
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from streams import blocks

# Snippet Models
@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    
    panels = [
        MultiFieldPanel([
            FieldPanel("name"),
            FieldPanel("image"),
        ], heading="Author's Name and Image"),
    ]
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(max_length=100, blank=False, null=False)
    
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]



# Orderable Models
class AuthorOrderable(Orderable):
    page = ParentalKey("blog.BlogDetailPage", related_name="blog_authors")
    author = models.ForeignKey("blog.Author", on_delete=models.CASCADE, related_name="+")
    
    panels = [
        FieldPanel("author"),
    ]
    

# Pages
class BlogsPage(RoutablePageMixin, Page):
    custom_title = models.CharField(max_length=100, blank=False, null=False, help_text='Custom title for the blog detail page')

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
    ]
    
    
    def get_context(self, request, *args, **kwargs):
        category_filter = request.GET.get('category')
        
        context = super().get_context(request, *args, **kwargs)
        context["blogs"] = BlogDetailPage.objects.live().public().order_by('-last_published_at')
        context["categories"] = Category.objects.all()
        
        if(category_filter):
            context["blogs"] = context["blogs"].filter(categories__name__contains=category_filter)
            
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
    categories = ParentalManyToManyField("blog.Category", blank=True)
    
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
        MultiFieldPanel([
            InlinePanel('blog_authors', label="Author", min_num=1),
        ], heading="Author(s)"),
        MultiFieldPanel([
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Category(s)"),
    ]
    
    
    
    
    
    
    
    
    
    
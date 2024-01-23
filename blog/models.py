from django.db import models
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.snippets.models import register_snippet
from wagtail.images.api.fields import ImageRenditionField
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.api import APIField

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
    

        
    @property
    def author_info(self):
        return {
            "id": self.author.id,
            "name": self.author.name,
            "image": {
                "title": self.author.image.title,
                "url": self.author.image.file.url,
                "width": self.author.image.width,
                "height": self.author.image.height,
            } if self.author.image else None,
        }
        
    # This additional "author_image" field is added just to use the "ImageRenditionField"
    @property
    def author_image(self):
        return self.author.image
    
    api_fields = [
        APIField("author_info"),
        APIField("author_image", serializer=ImageRenditionField('fill-200x200')),
    ]
    
# Tags
class Tag(TaggedItemBase):
    content_object = ParentalKey('blog.BlogDetailPage', on_delete=models.CASCADE, related_name='tagged_items')

# Pages
class BlogsPage(RoutablePageMixin, Page):
    custom_title = models.CharField(max_length=100, blank=False, null=False, help_text='Custom title for the blog detail page')

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
    ]
    
    
    def get_context(self, request, *args, **kwargs):
        category_filter = request.GET.get('category')
        
        context = super().get_context(request, *args, **kwargs)
        
        # context["blogs"] = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        # Pagination
        blogs = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        ## Category filtering
        if(category_filter and category_filter != "all"): 
            blogs = blogs.filter(categories__slug__exact=category_filter)
            
        ## Tag filtering
        tag = request.GET.get('tag')
        if(tag):
            blogs = blogs.filter(tags__slug=tag)
        
        paginator = Paginator(blogs, 2)
        page = request.GET.get("page")
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
        
        context["blogs"] = blogs    
        context["categories"] = Category.objects.all()
    
            
        return context
    
    
    @path('latest/<int:num>/', name='latest_blogs')
    @path('latest/', name='latest_blogs')
    def latest_blogs(self, request, num=1):
        self.custom_title = "Latest Blogs"
        
        return self.render(
            request,
            template="blog/latest_blogs.html",
            context_overrides={
                "blogs": BlogDetailPage.objects.live().public().order_by('-first_published_at')[:num],
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
    
    tags = ClusterTaggableManager(through=Tag, blank=True)
    
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
        MultiFieldPanel([
            FieldPanel('tags'),
        ], heading="Tag(s)"),
    ]
    
    api_fields = [
        APIField("custom_title"),
        APIField("categories"),
        APIField("content"),
        APIField("image"),
        APIField("blog_authors"),
    ]
    
    def save(self, *args, **kwargs):
        cacheKey = make_template_fragment_key(
            "blog_item_preview",
            [self.id],
        )
        cache.delete(cacheKey)
        return super().save(*args, **kwargs)
    
    
    
    
    
    
    
    
    
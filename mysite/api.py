from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet, BaseAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet

from rest_framework import serializers

from blog.models import Category


# # Create Custom API Views
# class CategorySerializer(serializers.ModelSerializer):    
#     class Meta(serializers.SerializerMetaclass):
#         model = Category
#         fields = '__all__'
          
# class BlogCategories(BaseAPIViewSet):
#     model = Category

#     # "base_serializer_class" used as a getter function not as a field to ensure that your Serializer
#     # is used directly without any additional fields being added automatically as 'type'
#     def get_serializer_class(self):
#         return CategorySerializer


# Create Router and Register API routes
api_router = WagtailAPIRouter("wagtailapi")
# api_router.register_endpoint("categories", BlogCategories)
api_router.register_endpoint("pages", PagesAPIViewSet)
api_router.register_endpoint("images", ImagesAPIViewSet)
api_router.register_endpoint("documents", DocumentsAPIViewSet)
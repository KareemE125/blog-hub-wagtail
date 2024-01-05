from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Subscriber

class SubscriberAdmin(ModelAdmin):
    model = Subscriber
    menu_label = "Subscribers"
    menu_icon = "mail"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("email", "name", "data_join")
    search_fields = ("email", "name")
    list_filter = ("name",)
    ordering = ("-data_join",)
    
    
    
modeladmin_register(SubscriberAdmin)
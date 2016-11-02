from django.contrib import admin
from core.models import Item, Image

class ItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(Item, ItemAdmin)

class ImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Image, ImageAdmin)

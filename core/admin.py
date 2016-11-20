from django.contrib import admin
from core.models import Item, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class ItemAdmin(admin.ModelAdmin):
    inlines = (ImageInline, )
    pass

admin.site.register(Item, ItemAdmin)

class ImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Image, ImageAdmin)

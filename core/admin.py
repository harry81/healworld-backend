from django.contrib import admin
from core.models import User, Item, Image

class UserAdmin(admin.ModelAdmin):
    model = User

admin.site.register(User, UserAdmin)

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

from django.contrib import admin
from scraper.models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "from_name", "item_type", "created_at")


admin.site.register(Item, ItemAdmin)

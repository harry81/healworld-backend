from django.contrib import admin
from scraper.models import ScraperItem


class ScraperItemAdmin(admin.ModelAdmin):
    list_display = ("id", "from_name", "item_type", "created_at")


admin.site.register(ScraperItem, ScraperItemAdmin)

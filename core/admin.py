from django.contrib import admin
from core.models import User, Item, Image
from fsm_admin.mixins import FSMTransitionMixin


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "profile_picture", "notification")

    def notification(self, instance):
        return True if instance.notification_push else ''

    model = User


admin.site.register(User, UserAdmin)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class ItemAdmin(FSMTransitionMixin, admin.ModelAdmin):
    inlines = (ImageInline, )
    list_display = ("image_tag", "user", 'state', "title",
                    "memo", "address", "created_at")
    fields = ("title", "memo", "user", "price", )
    list_filter = ('state',)
    fsm_field = ['state', ]

    def image_tag(self, instance):
        try:
            image = instance.images.all()[0]
            thumbnail = image.itemshot.thumbnail['50x50']
            url = "<img src=%s>" % thumbnail
            return url
        except IndexError:
            return ''

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

admin.site.register(Item, ItemAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Image, ImageAdmin)

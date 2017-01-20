from django.contrib import admin
from django_comments.admin import CommentsAdmin
from django_comments.models import Comment
from core.models import User, Item, Image
from fsm_admin.mixins import FSMTransitionMixin


class CommentCoreAdmin(CommentsAdmin):
    list_display = ('comment',) + CommentsAdmin.list_display


admin.site.unregister(Comment)
admin.site.register(Comment, CommentCoreAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ("profile_picture_url_tag", "username",
                    "last_login",
                    "profile_picture", "notification")

    def profile_picture_url_tag(self, instance):
        image = instance.profile_picture_url
        url = "<img src=%s width='40px'>" % image
        return url

    profile_picture_url_tag.short_description = 'Profile picture'
    profile_picture_url_tag.allow_tags = True

    def notification(self, instance):
        return instance.notification_push[0:10]\
            if instance.notification_push else ''

    model = User


admin.site.register(User, UserAdmin)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


def mark_deleted(modeladmin, request, queryset):
    queryset.update(deleted=True)

mark_deleted.short_description = "Mark as deleted"


class ItemAdmin(FSMTransitionMixin, admin.ModelAdmin):
    inlines = (ImageInline, )
    list_display = ("image_tag", "user", 'state', "title",
                    "memo", "address", "created_at")
    fields = ("title", "memo", "user", "price", 'deleted')
    list_filter = ('state', 'deleted')
    fsm_field = ['state', ]
    actions = [mark_deleted]

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

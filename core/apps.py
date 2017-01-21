from __future__ import unicode_literals

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from actstream import registry
        from django_comments.models import Comment

        registry.register(self.get_model('User'))
        registry.register(self.get_model('Item'))
        registry.register(Comment)

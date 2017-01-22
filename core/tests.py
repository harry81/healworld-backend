from django.test import TestCase
from core.models import User, Item
from django_comments.models import Comment


class CoreTests(TestCase):

    fixtures = ['core.json', ]

    def test_comment(self):
        import ipdb; ipdb.set_trace()
        print 'hi'

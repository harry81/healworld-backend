from django.test import TestCase
from core.models import User, Item
from django_comments.models import Comment
from .utils import get_short_url


class CoreTests(TestCase):

    fixtures = ['core.json', ]

    def test_comment(self):
        print 'hi'

    def test_short_url(self):
        short_url = get_short_url('hi')
        self.assertIn('me2', short_url)

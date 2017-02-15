from django.test import TestCase
from django_dynamic_fixture import G
from core.models import User, Item
from django_comments.models import Comment
from .utils import get_short_url
from django.test import Client


class CoreTests(TestCase):

    fixtures = ['core.json', ]

    def setUp(self):
        self.client = Client()

        self.user1 = G(User, phone='0001')
        self.user2 = G(User, phone='0002')
        self.user3 = G(User, phone='0003')

        self.item = G(Item, user=self.user1, ignore_fields=['state', ])

    def test_comment(self):
        self.client.force_login(self.user1)
        import ipdb; ipdb.set_trace()
        response = self.client.post('/api-comment/', {
            "comment": "h4llo",
            "content_type": 8,
            "site": 1,
            "user_name": "Harry Choi",
            "user": self.user1.id,
            "object_pk": self.item.id
        })
        self.assertEqual(response.status_code, 201)

    def test_short_url(self):
        short_url = get_short_url('hi')
        self.assertIn('me2', short_url)

    def test_registration_user(self):
        response = self.client.post('/rest-auth/registration/', {
            'username': 'john',
            'password1': 'smith1234',
            'password2': 'smith1234',
            'verified_code': '7234'
        })
        self.assertEqual(response.status_code, 201)

        user = User.objects.get(username='john')
        self.assertIsInstance(user, User)

    def test_registration_user_with_wrong_verified_code(self):
        response = self.client.post('/rest-auth/registration/', {
            'username': 'john',
            'password1': 'smith1234',
            'password2': 'smith1234',
            'verified_code': '1234'
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(0, User.objects.filter(username='john').count())

    def test_login(self):
        response = self.client.post('/rest-auth/registration/', {
            'username': 'john',
            'password1': 'smith1234',
            'password2': 'smith1234',
            'verified_code': '7234'
        })
        self.assertEqual(response.status_code, 201)

        user = User.objects.get(username='john')
        self.assertIsInstance(user, User)

        response = self.client.post('/rest-auth/login/', {
            'username': 'john',
            'password': 'smith1234',
        })
        self.assertEqual(response.status_code, 200)

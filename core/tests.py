from django.test import TestCase
from core.models import User
from .utils import get_short_url
from django.test import Client


class CoreTests(TestCase):

    fixtures = ['core.json', ]
    client = Client()

    def test_comment(self):
        print 'hi'

    def test_image_post(self):
        with open('/home/harry/Pictures/Yellowstone National.jpg') as fp:
            response = self.client.post('/api-image/', {
                'itemshot': fp,
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

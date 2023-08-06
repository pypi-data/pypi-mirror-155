from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse

from model_bakery import baker


class LoginTestCase(TestCase):
    def setUp(self):
        self.staff_user = baker.make(
            'auth.User',
            username='user',
            user_roles__role='staff',
        )
        self.password = 'password'
        self.staff_user.set_password(self.password)
        self.staff_user.save()

        self.login_url = reverse('gas:login')

    def test_redirect(self):
        client = Client()

        # with next parametter redirects to custom url
        response = client.post(self.login_url, {
            'next': 'next_url',
            'username': self.staff_user.username,
            'password': self.password,
            'is_active': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'next_url')

        # with no next parametter redirects to default url
        response = client.post(self.login_url, {
            'username': self.staff_user.username,
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('gas:index'))

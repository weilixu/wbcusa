from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings

class SignupViewTestCase(TestCase):

    def test_get(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        data = {
            "username": "foo",
            "password": "bar",
            "password_confirm": "bar",
            "email": "foobar@example.com"
        }

        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, 200)


class LoginViewTestCase(TestCase):
    def signup(self):
        data = {
            "username": "foo",
            "password": "bar",
            "password_confirm": "bar",
            "email": "foobar@example.com",
        }
        self.client.post(reverse("register"), data)
        self.client.logout()

    def test_get(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ["account/login.html"])

    def test_post_empty(self):
        data = {}
        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["form"].is_valid())

    def test_post_success_username(self):
        self.signup()
        data = {
            "username": "foo",
            "password": "bar",
        }
        response = self.client.post(reverse("login"), data)
        self.assertRedirects(
            response,
            settings.ACCOUNT_LOGIN_REDIRECT_URL,
            fetch_redirect_response=False
        )

    def test_post_success_email(self):
        self.signup()
        data = {
            "username": "foobar@example.com",
            "password": "bar",
        }
        response = self.client.post(reverse("login"), data)
        self.assertRedirects(
            response,
            settings.ACCOUNT_LOGIN_REDIRECT_URL,
            fetch_redirect_response=False
        )


class ProfileViewTestCase(TestCase):
    def signup(self):
        data = {
            "username": "foo",
            "password": "bar",
            "password_confirm": "bar",
            "email": "foobar@example.com",
        }
        self.client.post(reverse("register"), data)
        self.client.logout()


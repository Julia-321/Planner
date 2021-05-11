from django.contrib.auth.models import User
from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse
from accounts.models import Profile
from accounts.views import SignUpView
from django.test import Client


class AccountsTest(TestCase):

    def test_create_user(self):

        # without email
        User.objects.create(username="username", password="password")
        self.assertEqual(User.objects.count(), 1)

        User.objects.create(username="username2", email="email@email.com",  password="password")
        self.assertEqual(User.objects.count(), 2)

        # the same username
        error = False
        exc = None
        try:
            User.objects.create(username="username", password="password")
        except Exception as e:
            exc = e
            error = True
        self.assertTrue(error)
        self.assertTrue(isinstance(exc, IntegrityError))

    def test_create_profile(self):

        user = User.objects.create(username="username", password="password")
        Profile.objects.create(user=user)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first().user, user)

    def test_settings(self):

        user = User.objects.create(username="username", password="password")
        profile = Profile.objects.create(user=user)

        self.assertEqual(profile.notification_option, 1)
        self.assertEqual(profile.home_view, 1)
        self.assertEqual(profile.theme, 1)
        self.assertEqual(profile.push_time, 1)
        self.assertEqual(profile.date_view, 1)

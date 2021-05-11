from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import Profile
from tasks.models import Task
from django.utils import timezone


class TasksTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        user = User.objects.create(username="username", password="password")
        Profile.objects.create(user=user)

    def test_setup(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

    def test_create_task(self):

        test_time = timezone.now()
        task = Task.objects.create(user=User.objects.first(), name='title',
                                   description="description",
                                   deadline=test_time,
                                   complete=False)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(task.user, User.objects.first())
        self.assertEqual(task.name, "title")
        self.assertEqual(task.description, "description")
        self.assertEqual(task.deadline, test_time)
        self.assertFalse(task.complete)
        self.assertTrue(task.created < timezone.now())

        # without description

        test_time = timezone.now()
        task = Task.objects.create(user=User.objects.first(), name='title',
                                   deadline=test_time,
                                   complete=False)

        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(task.description, "")

        # without deadline

        task = Task.objects.create(user=User.objects.first(), name='title', complete=False)

        self.assertEqual(Task.objects.count(), 3)
        self.assertTrue(task.deadline)

        # without complete

        task = Task.objects.create(user=User.objects.first(), name='title')
        self.assertEqual(Task.objects.count(), 4)
        self.assertFalse(task.complete)

    def test_del_task(self):

        task = Task.objects.create(user=User.objects.first(), name='title')
        self.assertEqual(Task.objects.count(), 1)

        task.delete()
        self.assertEqual(Task.objects.count(), 0)

    def test_add_task_view(self):

        client = Client()
        client.force_login(User.objects.first())

        url = reverse('add_task')

        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], "text/html; charset=utf-8")

        response = client.post(url, data={'title': 'title', 'description': ''})

        self.assertEqual(response.status_code, 302)  # expected redirect
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().name, 'title')
        self.assertEqual(Task.objects.first().description, '')

        response = client.post(url, data={'title': 'title', 'description': 'desc'})

        self.assertEqual(response.status_code, 302)  # expected redirect
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.last().description, 'desc')

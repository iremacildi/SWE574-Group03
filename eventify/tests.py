from collections import UserDict
from datetime import date, datetime, time
from django.test import TestCase
from django.utils import timezone
from eventify.models import Post,Service
from django.contrib.auth.models import User
from django.test.client import Client

class EventTestCase(TestCase):   
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')


    def test_eventCreate(self):
        user = User.objects.get(username='testuser')
        self.client.login(username="testuser",password="12345")
        Post.objects.create(
        title="Event #1",
        content="Random Content",
        duration=2,
        eventdate="2021-11-20",
        eventtime="05:00:00",
        capacity=2,
        date_posted="2021-11-28 01:54:25.954935+03",
        paid=False,
        author_id=user.id,
        location="Istanbul",
        category="Seminar")

        event=Post.objects.get(title="Event #1")
        self.assertEqual(event.title, "Event #1")
        self.assertEqual(event.location, "Istanbul")
        Post.objects.get(title="Event #1").delete()


    def test_eventDelete(self):
        user = User.objects.get(username='testuser')
        self.client.login(username="testuser",password="12345")
        Post.objects.create(
        title="Event #1",
        content="Random Content",
        duration=2,
        eventdate="2021-11-20",
        eventtime="05:00:00",
        capacity=2,
        date_posted="2021-11-28 01:54:25.954935+03",
        paid=False,
        author_id=user.id,
        location="Istanbul",
        category="Seminar")

        event=Post.objects.get(title="Event #1")
        self.assertEqual(event.title, "Event #1")
        self.assertEqual(event.location, "Istanbul")
        Post.objects.get(title="Event #1").delete()

    def test_eventUpdate(self):
        user = User.objects.get(username='testuser')
        self.client.login(username="testuser",password="12345")
        Post.objects.create(
        title="Event #1",
        content="Random Content",
        duration=2,
        eventdate="2021-11-20",
        eventtime="05:00:00",
        capacity=2,
        date_posted="2021-11-28 01:54:25.954935+03",
        paid=False,
        author_id=user.id,
        location="Istanbul",
        category="Seminar")

        event=Post.objects.get(title="Event #1")
        event.title="Event #2"
        event.save()
        self.assertEqual(event.title, "Event #2")
        
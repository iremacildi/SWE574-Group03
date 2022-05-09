
from django.test import TestCase
from django.urls import reverse
from eventify.models import Service, Post, ServiceComment, Approved,RegisterEvent,RegisterService,Comment
from eventify.forms import PostForm, ServiceForm
from django.contrib.auth.models import User
from datetime import datetime

class AppliedEventsServicesViewTest(TestCase):
    def test_only_applied_events_in_list(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user1.save()
        test_user2.save()

        test_event = Post.objects.create( 
            author=test_user1, 
            title='EventTestObject - SET UP',
            content='Event Test Description - SET UP', 
            picture='uploads/event_pictures/default.png',
            location='41.0255493,28.9742571',
            category = 'Seminar',
            eventtime = '15:00:00',
            duration=3,
            date_posted='2022-05-03 09:18:03.100026+04', 
            eventdate='2022-06-10',
            capacity=21,
            paid = False,
            isLate = False,
            IsCancelled = False,
            )
        test_event.save()

        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')

        response = self.client.get(reverse('services'))
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertEqual(response.status_code, 200)
       

        test_service = Service.objects.create( 
        author=test_user2, 
        title='ServiceTestObject - SET UP',
        content='Service Test Description - SET UP', 
        picture='uploads/event_pictures/default.png',
        location='41.0255493,28.9742571',
        category = 'Seminar',
        eventtime = '15:00:00',
        duration=2,
        date_posted='2022-05-04 17:28:06.620026+03', 
        eventdate='2022-05-26',
        capacity=10,
        paid = False,
        isLate = False,
        isGiven = False,
        IsCancelled = False,
        )
        test_service.save()

        response = self.client.get(reverse('index'))
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertEqual(response.status_code, 200)

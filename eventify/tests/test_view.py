
from django.test import RequestFactory, TestCase
from django.urls import reverse
from eventify.models import Service, Post, ServiceComment, Approved,RegisterEvent,RegisterService,Comment
from eventify.views import ServiceCreateView, ServiceDetailView,PostDetailView
from eventify.forms import PostForm, ServiceForm
from django.contrib.auth.models import User
from datetime import datetime

class AppliedEventsServicesViewTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.factory = RequestFactory()
        self.test_user1 = User.objects.create(username='testuser1')
        self.test_user2 = User.objects.create(username='testuser2')
         # test_user1.save()
        # test_user2.save()

        self.test_event = Post.objects.create( 
            author=self.test_user1, 
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

        self.test_service = Service.objects.create( 
            author=self.test_user2, 
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
        
        self.test_service_form_data =  {
                'author':'self.test_user2',
                'title':'ServiceTestObject - SET UP',
                'content':'Service Test Description - SET UP', 
                'picture':'uploads/event_pictures/default.png',
                'location':'41.0255493,28.9742571',
                'category':'Seminar',
                'eventtime':'15:00:00',
                'duration':'2',
                'date_posted':'2022-05-04 17:28:06.620026+03', 
                'eventdate':'2022-05-26',
                'capacity':'10',
                'paid':'False',
                'isLate':'False',
                'isGiven': 'False',
                'IsCancelled':'False'}
        
        self.test_event_form_data =  {
                'author':'self.test_user2',
                'title':'ServiceTestObject - SET UP',
                'content':'Service Test Description - SET UP', 
                'picture':'uploads/event_pictures/default.png',
                'location':'41.0255493,28.9742571',
                'category':'Seminar',
                'eventtime':'15:00:00',
                'duration':'2',
                'date_posted':'2022-05-04 17:28:06.620026+03', 
                'eventdate':'2022-05-26',
                'capacity':'10',
                'paid':'False',
                'isLate':'False',
                'IsCancelled':'False'}


    def test_service_list(self):
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)
         
    def test_event_list(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        # response = self.client.get(reverse('service_detail', args=['1']))
        # self.assertEqual(str(response.context['address']), '41.0255493,28.9742571')
        response_about = self.client.get(reverse('about'))
        self.assertEqual(response_about.status_code, 200)
        # self.assertTrue(response_about.context['isLate']== False) 
        # self.assertTemplateUsed(response_about.status_code, 'eventify/about')


        # response_register_event = self.client.get(reverse('post_detail', args=['1']))

    def test_update_service(self):
        response = self.client.post(
            reverse('service_update', kwargs={'pk':1}),
            {'author':'self.test_user2',
               'title':'ServiceTestObject - SET UP',
                'content':'Service Test Description - SET UP', 
                'picture':'uploads/event_pictures/default.png',
                'location':'41.0255493,28.9742571',
                'category':'Seminar',
                'eventtime':'15:00:00',
                'duration':'2',
                'date_posted':'2022-05-04 17:28:06.620026+03', 
                'eventdate':'2022-05-26',
                'capacity':'10',
                'paid':'False',
                'isLate':'False',
                'isGiven':'False',
                'IsCancelled':'False'})
        self.assertEqual(response.status_code, 302)

    def test_update_event(self):
        response = self.client.post(
            reverse('service_update', kwargs={'pk':1}),
            {'author':'self.test_user2',
               'title':'ServiceTestObject - SET UP',
                'content':'Service Test Description - SET UP', 
                'picture':'uploads/event_pictures/default.png',
                'location':'41.0255493,28.9742571',
                'category':'Seminar',
                'eventtime':'15:00:00',
                'duration':'2',
                'date_posted':'2022-05-04 17:28:06.620026+03', 
                'eventdate':'2022-05-26',
                'capacity':'10',
                'paid':'False',
                'isLate':'False',
                'IsCancelled':'False'})
        self.assertEqual(response.status_code, 302)

    def test_create_service(self):
        form = ServiceCreateView(data = self.test_service_form_data)
        self.assertTrue(form.form_valid)

    def test_create_event(self):
        form = ServiceCreateView(data = self.test_event_form_data)
        self.assertTrue(form.form_valid)



from django.test import TestCase
from django.urls import reverse, resolve


from django.contrib.auth.models import User
from eventify.models import Service, Post
from eventify.views import ServiceCreateView, PostCreateView, ServiceDetailView

 
class URLTests(TestCase):
        

    def test_service_create_url_resolves(self):
        url = reverse('service_create')
        self.assertEquals(resolve(url).func.view_class, ServiceCreateView)
    
    def test_event_create_url_resolves(self):
        url = reverse('post_create')
        self.assertEquals(resolve(url).func.view_class, PostCreateView)

    def test_service_detail_url_resolves(self):
        test_user1 = User.objects.create_user(username='testuser1', password='k!j101112A')
        test_user1.save()
        
        test_service = Service.objects.create( 
                author=test_user1, 
                title='ServiceTestObject - SET UP',
                content='Service Test Description - SET UP', 
                picture='uploads/event_pictures/default.png',
                location='41.0255493,28.9742571',
                category = 'Art',
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

        url = reverse('service_detail', args=[str(test_service.pk)])
        self.assertEquals(resolve(url).func.view_class, ServiceDetailView)
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from eventify.models import Event, Offer
from eventify.views import EventCreateView, EventDetailView, OfferCreateView, ProfileView
import datetime
 

class URLTests(TestCase):
        
    def test_profile_url_resolves(self):
        test_user1 = User.objects.create_user(username='username1', password='q1w2e3r4')
        test_user1.save()
        url = reverse('profile', args=[str(test_user1.pk)])
        self.assertEquals(resolve(url).func.view_class, ProfileView)
    
    def test_event_create_url_resolves(self):
        url = reverse('event-create')
        self.assertEquals(resolve(url).func.view_class, EventCreateView)

   
    def test_event_detail_url_resolves(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1234dfxtxK')
        test_user1.save()

        test_event = Event.objects.create(
            eventOwner=test_user1, 
            eventCreatedDate='2021-01-01 10:00:00+03', 
            eventName="testevent",
            eventDescription="descr", 
            eventPicture='uploads/event_pictures/default.png',
            eventLocation='39.0255593,26.9872511',
            eventDate='2022-01-01',
            eventTime='11:22:00+00',
            eventCapacity=10,
            eventDuration=2
        )
        test_event.save()

        url = reverse('event-detail', args=[str(test_event.pk)])
        self.assertEquals(resolve(url).func.view_class, EventDetailView)

    def test_offer_create_url_resolves(self):
        url = reverse('offer-create')
        self.assertEquals(resolve(url).func.view_class, OfferCreateView)

   
    def test_offer_detail_url_resolves(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1234dfxtxK')
        test_user1.save()

        test_offer = Offer.objects.create(
            offerOwner=test_user1, 
            offerCreatedDate='2021-01-01 10:00:00+03', 
            offerName="testoffer",
            offerDescription="descr", 
            offerPicture='uploads/offer_pictures/default.png',
            offerLocation='39.0255593,26.9872511',
            offerDate='2022-01-01',
            offerTime='11:22:00+00',
            offerCapacity=10,
            offerDuration=2
        )
        test_offer.save()

        url = reverse('event-detail', args=[str(test_offer.pk)])
        self.assertEquals(resolve(url).func.view_class, EventDetailView)
   
   
   
   
   

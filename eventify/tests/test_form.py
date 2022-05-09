 
from eventify.forms import PostForm, ServiceForm
from eventify.models import Service
import datetime
from django.test import TestCase
from django.contrib.auth.models import User


#'title','duration','eventdate','category','eventtime','location','content','picture','capacity'

class ServiceFormTest(TestCase):

    def setUp(self):
       
        test_user1 = User.objects.create_user(username='testuser1', password='1q!190Art')

   
    def test_service_form__title_valid(self):

        # date = '2022-05-26'
        # form = ServiceForm(data={'eventdate': date})

        testForm = ServiceForm({
            'title ':'ServiceTestObject - SET UP',
            'content ':'Service Test Description - SET UP', 
            'location ':'41.0255493,28.9742571',
            'eventdate ': '2022-06-10',
            'eventtime': '15:00:00',
            'category':'Seminar', 
            'duration':'5',
            'capacity': '21',
            'picture ': 'uploads/event_pictures/default.png',
            


            })
        self.assertTrue(testForm.is_valid())


    
 
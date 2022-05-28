from ctypes import addressof
from datetime import datetime
from email.policy import default
from django.test import TestCase

from django.contrib.auth.models import User
from eventify.models import Service, Post, ServiceComment, Approved,RegisterEvent,RegisterService,Comment
from users.models import Profile

class ModelTest(TestCase):              
    @classmethod

    def setUp(self):
        self.userTestObject1 = User.objects.create(username='usertest')
        self.userTestObject2 = User.objects.create(username='usertest2')

       
        self.ServiceSetUpTestObject = Service.objects.create( 
            author=self.userTestObject1, 
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

        self.EventSetUpTestObject = Post.objects.create( 
            author=self.userTestObject1, 
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

  

    def testService(self):
        serviceTestObject = Service(
            author=self.userTestObject1, 
            date_posted=datetime.now, 
            title='ServiceTest',
            content='ServiceTestDescription', 
            # picture='uploads/event_pictures/default.png',
            location='41.0255493,28.9742571',
            eventdate=datetime.now,
            capacity=1,
            duration=1,
            )
        self.assertEqual(serviceTestObject.author, self.userTestObject1)
        self.assertEqual(serviceTestObject.date_posted, datetime.now)
        self.assertEqual(serviceTestObject.title, 'ServiceTest')
    
    def testPost(self):
        eventTestObject = Post(
            author=self.userTestObject1, 
            date_posted=datetime.now, 
            title='EventTest',
            content='EventTestDescription', 
            picture='uploads/event_pictures/default.png',
            location='41.0255493,28.9742571',
            eventdate=datetime.now,
            eventtime = '15:00:00',
            capacity=1,
            duration=10,
            paid = False,
            isLate = False,
            IsCancelled = False,
            tempLocation = 'TempLocationText'

            )
        self.assertEqual(eventTestObject.author, self.userTestObject1)
        self.assertEqual(eventTestObject.date_posted, datetime.now)
        self.assertEqual(eventTestObject.title, 'EventTest')
    
    def testServiceComment(self):
        serviceTestObject = ServiceComment(
            service = self.ServiceSetUpTestObject,
            author=self.userTestObject1, 
            text='EventTestDescription', 
            created_date = datetime.now,
            approved_comment = True
            )
        self.assertEqual(serviceTestObject.author, self.userTestObject1)
        self.assertEqual(serviceTestObject.text, 'EventTestDescription')

    def testApproved(self):
        approvedTestObject = Approved(
            service = self.ServiceSetUpTestObject,
            author=self.userTestObject1, 
            isOk='False', 
            created_date = datetime.now,
        )
        self.assertEqual(approvedTestObject.author, self.userTestObject1)
        self.assertEqual(approvedTestObject.isOk, 'False')

    def testRegisterEvent(self):
        registerEventTestObject = RegisterEvent(
            post = self.EventSetUpTestObject,
            author=self.userTestObject1, 
            username = 'usertest',
            title = 'Test Event Title - 4',
            created_date = datetime.now,
            approved_register= 'True',
        )
        self.assertEqual(registerEventTestObject.author, self.userTestObject1)
        self.assertEqual(registerEventTestObject.title, 'Test Event Title - 4')
    
    def testRegisterService(self):
        registerServiceTestObject = RegisterService(
            service = self.ServiceSetUpTestObject,
            author = self.userTestObject1, 
            username = 'usertest',
            title = 'Test Event Title - 4',
            owner = self.userTestObject2,
            created_date = datetime.now,
            approved_register= 'True',
        )
        self.assertNotEqual(registerServiceTestObject.author, self.userTestObject2)
        self.assertEqual(registerServiceTestObject.approved_register, 'True')
        self.assertEqual(registerServiceTestObject.title, 'Test Event Title - 4')

    def testComment(self):
        commentTestObject = Comment(
            post = self.EventSetUpTestObject,
            author = self.userTestObject1, 
            text = 'Test Service Comment - 4opjaidsjglşksdfnşg',
            created_date = datetime.now,
            approved_comment= 'True',
        )
        self.assertEqual(commentTestObject.author, self.userTestObject1)
        self.assertEqual(commentTestObject.approved_comment, 'True')

    def testProfile(self):
        profileTestObject = Profile(
            # history ='',
            user = self.userTestObject1,
            location = default,
            address = '',
            credits = '6',
            reserved = ''
        )
        self.assertEqual(profileTestObject.address, '')

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()

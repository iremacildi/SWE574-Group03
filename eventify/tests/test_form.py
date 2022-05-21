 
from eventify.forms import PostForm, ServiceForm
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

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
            'capacity': '20',
            'picture ': 'uploads/event_pictures/default.png',
            


            })
        self.assertFalse(testForm.is_valid())


    
 
 

##UserRegisterForm
#'first_name', -> Optional (blank=True). 150 characters or fewer.
# 'last_name', -> Optional (blank=True). 150 characters or fewer.
# 'username', -> Required. 150 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.
# 'email', -> Optional (blank=True). Email address.
# 'password1', 
# 'password2'

#Active Password validators -> check Validator for details in https://docs.djangoproject.com/en/4.0/topics/auth/passwords/
#UserAttributeSimilarityValidator, which checks the similarity between the password and a set of attributes of the user.
#MinimumLengthValidator, which checks whether the password meets a minimum length. This validator is configured with a custom option: 
                        #it now requires the minimum length to be nine characters, instead of the default eight.
#CommonPasswordValidator, which checks whether the password occurs in a list of common passwords. By default, it compares to an included list of 20,000 common passwords.
#NumericPasswordValidator, which checks whether the password isn’t entirely numeric.

##UserUpdateForm
#'first_name','last_name','username', 'email'

##ProfileUpdateForm
#'location','image'

class UserRegisterFormTest(TestCase):

    def setUp(self):
       
        test_user1 = User.objects.create_user(username='testuser1', password='1q!190Art')

   
    def test_user_form__email_not_valid(self):

        testUserForm = UserRegisterForm(data = {
            'first_name':'Arnold',
            'last_name':'Schwarzenegger', 
            'username':'ArnoldSchwarzenegger',
            'email':'ArnoldSchwarzenegger@',
            'password1': '2@Mt,Aj~',
            'password2':'2@Mt,Aj~', 
            })
        self.assertFalse(testUserForm.is_valid())
    
    def test_user_form_first_last_name_valid(self):

        testUserForm2 = UserRegisterForm(data = {
            'first_name ':'Arnold',
            'last_name ':'Schwarzenegger', 
            'username':'ArnoldSchwarzenegger',
            'email':'arnoldschwarzenegger@gmail.com',
            'password1': '2@Mt,Aj~',
            'password2':'2@Mt,Aj~', 
            })
        self.assertTrue(testUserForm2.is_valid())

    
 

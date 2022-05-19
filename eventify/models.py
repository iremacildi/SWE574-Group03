from django.db import models
from django.db.models.fields import BooleanField
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from location_field.models.plain import PlainLocationField
from simple_history.models import HistoricalRecords


CATEGORY_CHOICE = (
    ('Seminar','Seminar'),
    ('Conference', 'Conference'),
    ('Workshop','Workshop'),
    ('Themed party','Themed Party'),
    ('Webinar','Webinar'),
    ('Summit','Summit'),
    ('Music festival','Music Festival'),)
        

def upload_post_to(instance,filename):
	return f'post_picture/{instance.user.username}/{filename}'


class Post(models.Model):
    history = HistoricalRecords()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    location = PlainLocationField(default='41.088165, 29.043431', zoom=7, blank=False, null=False)
    content = models.TextField()
    tempLocation = models.TextField(blank=True)
    eventdate = models.DateField(default=timezone.now)
    eventtime=models.TimeField()
    category=models.CharField(max_length=20, choices=CATEGORY_CHOICE, default='Seminar')
    duration=models.IntegerField(default=1,validators=[MaxValueValidator(20), MinValueValidator(1)])
    capacity=models.IntegerField(default=1,validators=[MaxValueValidator(100), MinValueValidator(1)])
    picture = models.ImageField(upload_to='uploads/event_pictures/',blank=False)
    date_posted = models.DateTimeField(default=timezone.now)
    paid= models.BooleanField(default=False)
    IsCancelled= models.BooleanField(default=False)
    isLate=BooleanField(default=False)
   

    class Meta:
        ordering = ('-date_posted', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

class Service(models.Model):
    history = HistoricalRecords()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    eventdate = models.DateField(default=timezone.now)
    tempLocation = models.TextField(blank=True)
    eventtime=models.TimeField()
    duration=models.IntegerField(default=1,validators=[MaxValueValidator(20), MinValueValidator(1)])
    category=models.CharField(max_length=20, choices=CATEGORY_CHOICE, default='Seminar') 
    capacity=models.IntegerField(default=1,validators=[MaxValueValidator(20), MinValueValidator(1)])
    location = PlainLocationField(default='41.088165, 29.043431', zoom=7, blank=False, null=False)
    content = models.TextField()
    picture = models.ImageField(upload_to='uploads/event_pictures/',blank=False)
    date_posted = models.DateTimeField(default=timezone.now)
    paid= models.BooleanField(default=False)
    isLate=BooleanField(default=False)
    isGiven=BooleanField(default=False)
    IsCancelled= models.BooleanField(default=False)
    currentAtt=models.IntegerField(default=0)
 

    class Meta:
        ordering = ('-date_posted', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'pk': self.pk}) 

class ServiceComment(models.Model):
    history = HistoricalRecords()
    service = models.ForeignKey(Service, related_name='servicecomment', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("service_list")

    def __str__(self):
        return self.author

class Approved(models.Model):
    service = models.ForeignKey(Service, related_name='approved', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    isOk = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)


    def get_absolute_url(self):
        return reverse("service_list")

    def __str__(self):
        return self.author

class RegisterEvent(models.Model):
    post = models.ForeignKey(Post, related_name='postregister', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.TextField()
    title = models.CharField(max_length=100,blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    approved_register = models.BooleanField(default=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.author

class RegisterService(models.Model):
    service = models.ForeignKey(Service, related_name='serviceregister', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.TextField()
    title = models.CharField(max_length=100, blank=True)
    owner=models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    approved_register = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("service_list")

    def __str__(self):
        return self.author        

class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)
    history = HistoricalRecords()

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.author


class ServiceChart(models.Model):
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    min_attendee=models.IntegerField(default=0)
    max_attendee=models.IntegerField(default=0)

        
# class Friend(models.Model):
#     users = models.ManyToManyField(User)
#     current_user = models.ForeignKey(User, related_name='owner', null=True)

#     @classmethod
#     def make_friend(cls, current_user, new_friend):
#         friend = cls.objects.get_or_create(
#             current_user=current_user
#         )
#         friend.users.add(new_friend)

#     @classmethod
#     def lose_friend(cls, current_user, new_friend):
#         friend = cls.objects.get_or_create(
#             current_user=current_user
#         )
#         friend.users.remove(new_friend)
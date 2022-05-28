from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from location_field.models.plain import PlainLocationField
from simple_history.models import HistoricalRecords
from django.forms import CharField
from django.utils import timezone

INTEREST_CHOICES = (
        ('sport', 'Sport'),
        ('art', 'Art'),
        ('music', 'Music'),
        ('cooking', 'Cooking'),
        ('agriculture', 'Agriculture'),
        ('handicraft', 'Handicraft'),
        ('dance', 'Dance'),
        ('music', 'Music'),
        ('cinema', 'Cinema'),
        ('fashion', 'Fashion'),
)

class InterestSelection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    interest_1 = models.CharField(max_length=120, choices=INTEREST_CHOICES)
    interest_2 = models.CharField(max_length=120, choices=INTEREST_CHOICES)
    interest_3 = models.CharField(max_length=120, choices=INTEREST_CHOICES)

    def save(self, *args, **kwargs):
        super(InterestSelection, self).save(*args, **kwargs)

class Profile(models.Model):
    history = HistoricalRecords()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    location = PlainLocationField(default='41.088165, 29.043431', zoom=7, blank=False, null=False)
    address=models.TextField(blank=True)
    credits=models.IntegerField(default=6)
    reserved=models.IntegerField(default=0)
    interest=models.TextField(blank=True)
    isEmployee = models.BooleanField(default=False)
    created=models.DateField(default=timezone.now)
    range=models.IntegerField(default=1)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

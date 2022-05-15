from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from location_field.models.plain import PlainLocationField
from simple_history.models import HistoricalRecords


class Profile(models.Model):
    history = HistoricalRecords()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    location = PlainLocationField(default='41.088165, 29.043431', zoom=7, blank=False, null=False)
    address=models.TextField(blank=True)
    credits=models.IntegerField(default=6)
    reserved=models.IntegerField(default=0)
    interest=models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

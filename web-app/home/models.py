from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    isDriver = models.IntegerField(default = 0)

    def __str__(self):
        return self.user.username

class Vehicle(models.Model):
    #owner = models.OneToOneField(User,related_name="vehicle")#ForeignKey#on_delete=models.CASCADE,
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    driver_name = models.CharField(default='Name',max_length=50)
    car_type = models.CharField(default='Car',max_length=50)
    license_number = models.CharField(default='000',max_length=20)
    capacity = models.IntegerField(default=4)
    comment = models.TextField(blank=True, default="")

    def __str__(self):
        return self.driver_name
        #return f'{self.owner.username} Vehicle'

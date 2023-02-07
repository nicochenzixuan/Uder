from django.db import models
from django.contrib.auth.models import User

class DriverStatus(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    isDriver = models.IntegerField(default = 0)

    def __str__(self):
        return self.user.username

class Vehicle(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    driver_name = models.CharField(default='Name',max_length=50)
    capacity = models.IntegerField(default=5)
    car_type = models.CharField(default='Car',max_length=50)
    license_number = models.CharField(default='',max_length=20)
    description = models.CharField(default='',max_length=500)

    def __str__(self):
        return self.driver_name


class Ride(models.Model):
    #1st ele real value
    #2nd ele readable tag
    tags = (
        ('completed', 'completed'),
        ('confirmed', 'confirmed'),
        ('open', 'open'),
    )
    driver = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    owner= models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', null=True)
    status = models.CharField(choices=tags, default='open',max_length=50)
    sharer_list = models.ManyToManyField(User, blank=True, related_name='sharer_list')
    dest = models.CharField(max_length = 50)
    time_arrive = models.DateTimeField()
    numberOfPassenger = models.IntegerField(default=4)
    canShare = models.BooleanField()
    
    def __str__(self):
        return self.dest


from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Vehicle(models.Model):
    #owner = models.OneToOneField(User,related_name="vehicle")#ForeignKey#on_delete=models.CASCADE,
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    car_type = models.CharField(default='Car',max_length=50)
    license_number = models.CharField(default='000',max_length=20)
    capacity = models.IntegerField(default=4)
    comment = models.TextField(blank=True, default="")

    def __str__(self):
        return self.car_type
        #return f'{self.owner.username} Vehicle'

class Ride(models.Model):
#    owner = models.CharField(max_length = 50)
#    owner= models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    destination = models.CharField(max_length = 150)
    arrival_time = models.DateTimeField()
    numberOfPassenger = models.IntegerField(default=4)
    canShare = models.BooleanField()
    STATUS = (
        ('open', 'open'),
        ('confirmed', 'confirmed'),
        ('completed', 'completed'),
    )
    status = models.CharField(max_length=20, choices=STATUS, default='open')
    
    def __str__(self):
        return self.destination


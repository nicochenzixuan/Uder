from django.db import models

# Create your models here.

class Account(models.Model):
    #question_text = models.CharField(max_length=200)
    #pub_date = models.DateTimeField('date published')
    username = models.CharField(max_length=128, unique= True)
    password = models.CharField(max_length=256)
    
    def __str__(self):
        return self.username


class Vehicle(models.Model):
    driverName = models.CharField(default = "", max_length = 150)
    carType = models.CharField(default = "sedan", max_length=20)
    maxCapacity = models.IntegerField(default = 4)
    licensePlateNumber = models.CharField(default = "", max_length=10)

    def __str__(self):
        return self.v_type
        #return f'{self.owner.username} Vehicle'

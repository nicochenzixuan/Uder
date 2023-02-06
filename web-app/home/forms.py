#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Vehicle
from .models import Ride


# Create your forms here.

class NewUserForm(UserCreationForm):

    username = forms.CharField(required=True, max_length=20)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True, max_length=20)
    password2 = forms.CharField(required=True, max_length=20)

    class Meta:

        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class VehicleForm(forms.ModelForm):
    #owner = models.OneToOneField(User,on_delete=models.CASCADE,related_name="vehicle")#ForeignKey
    owner=User
    driver_name = forms.CharField(required=True)
    car_type = forms.CharField(required=True)
    license_number = forms.CharField(required=True)
    capacity = forms.IntegerField(required=True)
    comment = forms.CharField()
    
    class Meta:
        model = Vehicle 
        fields = ['owner','driver_name','car_type', 'license_number', 'capacity', 'comment']
    
    def save(self, commit=True):
        v = super(VehicleForm, self).save(commit=False)
        
        #v.car_type = self.cleaned_data['car_type']
        #v.license_number = self.cleaned_data['license_number']
        #v.capacity = self.cleaned_data['capacity']
        #v.comment = self.cleaned_data['comment']
        
        if commit:
            v.save()
        return v

class UserProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username','password','email']
    

class RequestForm(forms.ModelForm):
    owner = User
    destination = forms.CharField()
    arrival_time = forms.DateTimeField()
    numberOfPassenger = forms.IntegerField()
    canShare = forms.BooleanField(required=True)
    class Meta:
        model = Ride
        fields = ['destination', 'arrival_time', 'numberOfPassenger', 'canShare']

    
    

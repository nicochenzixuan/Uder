from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Vehicle, Ride

class UserForm(UserCreationForm):

    username = forms.CharField(required=True, max_length=20)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True, max_length=20)
    password2 = forms.CharField(required=True, max_length=20)

    class Meta:

        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class VehicleForm(forms.ModelForm):
    owner=User
    driver_name = forms.CharField(required=True)
    car_type = forms.CharField(required=True)
    license_number = forms.CharField(required=True)
    capacity = forms.IntegerField(required=True)
    description = forms.CharField()
    
    class Meta:
        model = Vehicle 
        fields = ['owner','driver_name','car_type', 'license_number', 'capacity', 'description']
    
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
    username = forms.CharField()
    #password = forms.CharField(required=True, max_length=20)
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username','email']
    
class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'
    
    
class RequestForm(forms.ModelForm):
    owner = User
    dest = forms.CharField()
    time_arrive = forms.DateTimeField(
    input_formats = ['%Y-%m-%dT%H:%M'],
        widget = DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
    
    
    )
    numberOfPassenger = forms.IntegerField()
    canShare = forms.BooleanField(required=False, initial=True)
    class Meta:
        model = Ride
        fields = ['dest', 'time_arrive', 'numberOfPassenger', 'canShare']
        

    
class ShareSearchForm(forms.Form):
    dest = forms.CharField()
    earliest_time = forms.DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
        )

    latest_time = forms.DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
        )
    numberOfPassenger = forms.IntegerField()

class DriverSearchForm(forms.Form):
    vehicle_capacity = forms.IntegerField()
    

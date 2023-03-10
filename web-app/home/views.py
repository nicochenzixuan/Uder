from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User


from django.shortcuts import  render, redirect, get_object_or_404
from .forms import NewUserForm,VehicleForm,UserProfileUpdateForm

from .models import Vehicle,UserProfile

from django.shortcuts import render,redirect, get_object_or_404

from .forms import RequestForm
from .models import Ride
import datetime
from django.utils import timezone

#from django.contrib.auth.forms import AuthenticationForm


def index(request):
    return HttpResponse("Hi this is my home page. I believe we will finally make it work.")

        
def login(request):
    template = loader.get_template('home/login.html')
    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                
                form = auth_login(request,user)
                #messages.success(request, f' welcome {username} !!')
                #messages.success(request, 'Successfully Login')
                return redirect('welcome')#should go to home page
                #return redirect('home/index.html')
            else:
                
                # Return an 'invalid login' error message.
                #messages.info(request, f'account does not exit plz sign in')
                messages.info(request, 'Error Login!! Plz try again or register')
                #return redirect('register')
                #raise Http404("Question does not exist")
    #form = AuthenticationForm()
    #return render(request, './templates/home/login.html')
    context = {}#context must be dict??  A context is a variable name -> variable value mapping that is passed to a template.
    return HttpResponse(template.render(context, request))
    #return HttpResponse("This is the login page!")

def register(request):
    if request.method == "POST":
        user_form = NewUserForm(request.POST) 
        #for field in user_form:
            #print("Field Error:", field.name,  field.errors)
        
        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)
            messages.success(request, "Registration successful." )
            
            print("important: register successful!") 
            return redirect('login')
                
        print("error: register not successful!")       
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    template = loader.get_template('home/register.html')
    context = {"register_form":form}
	  #return render (request=request, template_name="main/register.html", context={"register_form":form})
    return HttpResponse(template.render(context, request))
    


@login_required
def welcome(request):
    if not request.user.is_authenticated:
        return render(request, 'home/login.html')
    template = loader.get_template('home/welcome.html')
    context = {}
    return HttpResponse(template.render(context, request))


@login_required
def driver(request):

    if request.method == "POST":
        v_form = VehicleForm(request.POST) 
        print("important: where out") 
        if v_form.is_valid():
            
            #userProfile = UserProfile.objects.get(user=request.user)
            #userProfile.isDriver = 1
            #userProfile.save()
            
            v_form.save()
            
            messages.success(request, "Driver Registration successful." )
            
            print("important: driver register successful!") 
            return redirect('driver')
                
        print("error: register not successful!")       
        messages.error(request, "Unsuccessful registration. Invalid information.")
    v_form1 = VehicleForm()
    template =loader.get_template('home/driver.html')
    context = {"driver_form":v_form1}
    #context = {}
	  #return render (request=request, template_name="main/register.html", context={"register_form":form})
    return HttpResponse(template.render(context, request))

def profile(request):
    #userProfile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':

        #profileUpdateForm = UserProfileUpdateForm(request.POST)
        driverUpdateForm = VehicleForm(request.POST)
        #if(userProfile.isDriver==1):
        car = Vehicle.objects.get(driver_name=request.user.username)
        print(driverUpdateForm.is_valid())
        #driverUpdateForm1 = VehicleForm(instance=request.user.vehicle)
        #print(driverUpdateForm1.is_valid())
        #if driverUpdateForm.is_valid():
            #profileUpdateForm = UserProfileUpdateForm(instance=request.user)
            
        car_type = driverUpdateForm.cleaned_data.get('car_type')
        capacity = driverUpdateForm.cleaned_data.get('capacity')
            #if(maxCapacity<=0):
                #driverUpdateForm = DriverRegisterForm(instance=request.user.car)
                #context = {'profileUpdateForm':profileUpdateForm,'driverUpdateForm':driverUpdateForm,'prompt':"please select valid capacity!"}
                #return render(request,'profile.html',context)
        license_number = driverUpdateForm.cleaned_data.get('license_number')
        comment = driverUpdateForm.cleaned_data.get('comment')
        print("before i found it")
        v=Vehicle.objects.filter(driver_name=request.user.username)
        print("i found it")
        v.update(car_type = car_type, capacity = capacity,license_number = license_number,comment=comment)
            #driverUpdateForm.save()
            
        context = {'driverUpdateForm':driverUpdateForm,'prompt':"successfully update car info!"}
        template =loader.get_template('home/profile.html')
        return HttpResponse(template.render(context, request))

            #return render(request,'home/profile.html',context)
    else:
        #profileUpdateForm = UserProfileUpdateForm(instance=request.user)
        #driverUpdateForm = VehicleForm()
        #if(userProfile.isDriver==1):
        driverUpdateForm = VehicleForm(instance=request.user.vehicle)
    #context = {'profileUpdateForm':profileUpdateForm,'driverUpdateForm':driverUpdateForm}
    context = {'driverUpdateForm':driverUpdateForm}
    template =loader.get_template('home/profile.html')
    return HttpResponse(template.render(context, request))



@login_required
def ride_request(request):
    ride = Ride()
    if request.method == "POST":
        form = RequestForm(request.POST)
        print("important: where out")
        if form.is_valid():
            print("important: where 0")
            ride.destination = form.cleaned_data['destination']
            ride.arrival_time = form.cleaned_data['arrival_time']
            currenttime = timezone.now()
            if ride.arrival_time < currenttime:
                messages.warning(request, f'Your time is invalid')
                return render(request,'home/ride_request.html', {'form':form})
            print("important: where 1")
            ride.owner = request.user
            ride.numberOfPassenger = form.cleaned_data['numberOfPassenger']
            share = request.POST.get("can_Shared")
            if share == "no":
                ride.canShare = False
            else:
                ride.canShare = True
            ride.status = 'open'
            ride.save()
#            messages.success(request, "Request sent successful." )
            print("important: Request sent successful!")
            return redirect('welcome')
    else:
        form = RequestForm()
        print("error: request sent not successful!")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    return render(request, 'home/ride_request.html', {'form':form})

 #   template =loader.get_template('home/ride_request.html')
  #  context = {"ride_request_form":r_form1} 
   # return HttpResponse(template.render(context, request)) 

request_id = 0
@login_required
def ride_select(request):
    ride_own = list(Ride.objects.filter(owner=request.user).exclude(status='complete'))
    
 #   ride_sharer = list(Ride.objects.filter(sharer = request.user))
    context = {
        'ride_own': ride_own
#        'ride_share' : ride_sharer
    }

    if request.method == 'POST':
        request_id = request.POST['request_id']
        return redirect('edit_request')
#        return render(request, 'home/ride_select.html', context)
    
    return render(request, 'home/ride_select.html', context)

@login_required
def edit_request(request, request_id):
    ride = get_object_or_404(Ride, id=request_id)
    if request.method == 'POST':
        form = RequestForm(request.POST)
        print("errors")
        print(form.errors.as_data())
        if form.is_valid():
            if ride.status=='open':
                destination = form.cleaned_data.get('destination')
                numberOfPassenger = form.cleaned_data.get('numberOfPassenger')
                arrival_time= form.cleaned_data.get('arrival_time')

                ride = Ride.objects.filter(id=request_id) 
                ride.update(destination = destination, numberOfPassenger = numberOfPassenger, arrival_time = arrival_time)
                context = {'form':form,'prompt':"successfully update request!"}
                template =loader.get_template('home/edit_request.html')
                return HttpResponse(template.render(context, request))
            else:
                context = {'form':form,'prompt':"the request is not open, you cannot update!"}
                template =loader.get_template('home/edit_request.html')
                return HttpResponse(template.render(context, request))
    else:
#        ride = Ride.objects.filter(id=request_id)
        form = RequestForm(instance=ride)#instance.id==request_id)
    context = {'form':form}
    template =loader.get_template('home/edit_request.html')
    return HttpResponse(template.render(context, request))



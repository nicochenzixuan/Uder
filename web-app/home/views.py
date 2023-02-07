from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm,VehicleForm,UserProfileUpdateForm,RequestForm,ShareSearchForm,DriverSearchForm
from .models import Vehicle,DriverStatus,Ride
import datetime
from django.utils import timezone
from django.db.models import Q



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
                return redirect('welcome')
                
            else:
                
                messages.info(request, 'Error Login!! Plz try again or register')
                
    context = {}
    return HttpResponse(template.render(context, request))

def register(request):
    if request.method == "POST":
        user_form = UserForm(request.POST) 
        
        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)
            profile = DriverStatus(user=user, isDriver=0)
            profile.save()
            messages.success(request, "Registration successful." )
            
            print("important: register successful!") 
            return redirect('login')
                
        print("error: register not successful!")       
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserForm()
    template = loader.get_template('home/register.html')
    context = {"register_form":form}
	  #return render (request=request, template_name="main/register.html", context={"register_form":form})
    return HttpResponse(template.render(context, request))
    


@login_required
def welcome(request):
    
    template = loader.get_template('home/welcome.html')
    context = {}
    return HttpResponse(template.render(context, request))


@login_required
def driver(request):
    
    if request.method == "POST":
        
        f = VehicleForm(request.POST) 
        if(request.user.driverstatus.isDriver==1):
            return redirect('welcome')
        if f.is_valid():
            
            driverstatus = DriverStatus.objects.get(user=request.user)
            driverstatus.isDriver = 1
            driverstatus.save()
            
            f.save()
            
            messages.success(request, "Driver Registration successful." )
            
            print("important: driver register successful!") 
            return redirect('driver')
                
        print("error: register not successful!")       
        messages.error(request, "Unsuccessful registration. Invalid information.")
        
    f = VehicleForm()
    template =loader.get_template('home/driver.html')
    context = {"driver_form":f}
    return HttpResponse(template.render(context, request))

@login_required
def update_driver_info(request):
    driverstatus = DriverStatus.objects.get(user=request.user)
    if request.method == 'POST':

        profileUpdateForm = UserProfileUpdateForm(request.POST)
        
        if(driverstatus.isDriver==1):
            #car = Vehicle.objects.get(driver_name=request.user.username)
            driverUpdateForm = VehicleForm(request.POST)
            print("error car yes")
        else:
            driverUpdateForm = VehicleForm()
            print("error car no")
            
        print("errors")
        print(driverUpdateForm.errors.as_data())
        check=driverUpdateForm.is_valid()
        #if driverUpdateForm.is_valid():
            
        car_type = driverUpdateForm.cleaned_data.get('car_type')
        capacity = driverUpdateForm.cleaned_data.get('capacity')
        license_number = driverUpdateForm.cleaned_data.get('license_number')
        description = driverUpdateForm.cleaned_data.get('description')
        v=Vehicle.objects.filter(driver_name=request.user.username)
        v.update(car_type = car_type, capacity = capacity,license_number = license_number,description=description)
          
        context = {'driverUpdateForm':driverUpdateForm,'prompt':"successfully update car info!"}
        template =loader.get_template('home/profile.html')
        return HttpResponse(template.render(context, request))

            #return render(request,'home/profile.html',context)
    
    else:
        
        if(driverstatus.isDriver==1):
            driverUpdateForm = VehicleForm(instance=request.user.vehicle)
        else:
            context = {'prompt':"Not a Driver!"}
            template =loader.get_template('home/welcome.html')
            return HttpResponse(template.render(context, request))
            
    #context = {'profileUpdateForm':profileUpdateForm,'driverUpdateForm':driverUpdateForm}
    context = {'driverUpdateForm':driverUpdateForm}
    template =loader.get_template('home/profile.html')
    return HttpResponse(template.render(context, request))

@login_required
def update_user_info(request):
    
    if request.method == 'POST':
        
        user_form = UserProfileUpdateForm(request.POST)
            
            
        print("errors")
        print(user_form.errors.as_data())
        check=user_form.is_valid()
        print(user_form.is_valid())
        if user_form.is_valid():
            
            username_= user_form.cleaned_data['username']
            
            email_= user_form.cleaned_data['email']
            #password_= user_form.cleaned_data['password']
            
            #check_encrypted_password(pwd_old, user.password):
            #user.password = encrypt_password(pwd_new)
        
       
            u=User.objects.filter(username=request.user.username)
            u.update(username=username_, email = email_)#, password=password_
            v=Vehicle.objects.filter(driver_name=request.user.username)
            v.update(driver_name=username_)
          
        context = {'user_form':user_form,'prompt':"successfully update user info!"}
        template =loader.get_template('home/user_profile.html')
        return HttpResponse(template.render(context, request))
    
            
    #context = {'profileUpdateForm':profileUpdateForm,'driverUpdateForm':driverUpdateForm}
    else:
        user_form = UserProfileUpdateForm(instance=request.user)
        
    context = {'user_form':user_form}
    template =loader.get_template('home/user_profile.html')
    return HttpResponse(template.render(context, request))

@login_required
def delete_driver(request):
    driverstatus = DriverStatus.objects.get(user = request.user)
    if driverstatus.isDriver == 1:
        driverstatus.isDriver = 0
        driverstatus.save()
        Vehicle.objects.get(driver_name = request.user.username).delete()
    return render(request,'home/welcome.html',{'prompt':'Driver status canceled!'})
 
 
@login_required       
def user_logout(request):
    
    logout(request)
    return redirect('login')

@login_required
def start_ride(request):
    r = Ride()
    if request.method == "POST":
        form = RequestForm(request.POST)
        
        if form.is_valid():
            print("error")
            print(r)
            print(form)
            
            r.dest = form.cleaned_data['dest']
            r.time_arrive = form.cleaned_data['time_arrive']
            
            
            if r.time_arrive < timezone.now():
                context = {'form':form,'prompt':"Cannot choose time before now!"}
                return render(request,'home/start_ride.html', context)
            
            r.owner = request.user
            r.numberOfPassenger = form.cleaned_data['numberOfPassenger']
            share = request.POST.get("canShare")
            if share == None:
                r.canShare = False
            else:
                r.canShare = True
            r.status = 'open'
            r.save()
            
            return redirect('welcome')
    else:
        form = RequestForm()
        print("error: request sent not successful!")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    return render(request, 'home/start_ride.html', {'form':form})

request_id = 0
@login_required
def ride_select(request):
    ride_own = list(Ride.objects.filter(Q(owner=request.user) | Q(sharer_list = request.user)).exclude(status='complete'))
    
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
    r = get_object_or_404(Ride, id=request_id)
    if request.method == 'POST':
        form = RequestForm(request.POST)
        print("errors")
        print(form.errors.as_data())
        if form.is_valid():
            if r.status=='open':
                dest = form.cleaned_data.get('dest')
                numberOfPassenger = form.cleaned_data.get('numberOfPassenger')
                time_arrive= form.cleaned_data.get('time_arrive')
                canShare= form.cleaned_data.get('canShare')
                r = Ride.objects.filter(id=request_id) 
                r.update(dest = dest, numberOfPassenger = numberOfPassenger, time_arrive = time_arrive,canShare=canShare)
                context = {'form':form,'prompt':"successfully update request!"}
                template =loader.get_template('home/edit_request.html')
                return HttpResponse(template.render(context, request))
            else:
                context = {'form':form,'prompt':"the request is not open, you cannot update!"}
                template =loader.get_template('home/edit_request.html')
                return HttpResponse(template.render(context, request))
    else:

        form = RequestForm(instance=r)
    context = {'form':form}
    template =loader.get_template('home/edit_request.html')
    return HttpResponse(template.render(context, request))


@login_required
def share_search(request):
    #context = {}
    if(request.method == 'POST'):
        form = ShareSearchForm(request.POST)
        
        if form.is_valid():
            dest = form.cleaned_data['dest']
            early_time =  form.cleaned_data['earliest_time']
            late_time = form.cleaned_data['latest_time']
            numberOfPassenger = form.cleaned_data['numberOfPassenger']
            
            ride = Ride.objects.filter(
            time_arrive__range=(early_time,late_time), dest = dest, status = 'open',canShare = True)
            
            #context['rides']=ride
            return render(request, 'home/share_search_display.html', {'rides':ride})
    else :
        form = ShareSearchForm()
        return render(request, 'home/share_search.html', {'form':form})
        
@login_required
def driver_search(request):
    context = {}
    if(request.method == 'POST'):
        form = DriverSearchForm(request.POST)
        
        if form.is_valid():
            vehicle_capacity = form.cleaned_data['vehicle_capacity']
            
            if vehicle_capacity > request.user.vehicle.capacity:
                context = {'form':form,'prompt':"Larger than your car capacity!!!!!"}
                #messages.info(request, f'Larger than your car capacity!!!!!')
                template =loader.get_template('home/driver_search.html')
                
                return HttpResponse(template.render(context, request))
            ride = Ride.objects.filter(status = 'open',numberOfPassenger__lt=vehicle_capacity)#passenger_number__lte=request.user.vehicle.capacity
            
            context['rides']=ride
            print(ride)
            return render(request, 'home/driver_search_display.html', {'rides':ride})
    else :
        form = DriverSearchForm()
        return render(request, 'home/driver_search.html', {'form':form})
        
@login_required
def join_ride(request, request_id):
    ride = Ride.objects.filter(pk=request_id)[0]# need to get the first ele because this is a query set
    ride.sharer_list.add(request.user)
    #need update ride passen num
    #ride.numberOfPassenger=ride.numberOfPassenger+
    ride.save()
    return redirect('welcome')

@login_required
def confirm_request(request, request_id):
    ride = Ride.objects.filter(pk=request_id)[0]
    ride.status='confirmed'
    #bond driver ride together
    ride.driver=request.user
    ride.save()
    
    #send email
    email_receivers=[]
    email_receivers.append(ride.owner.email)
    for sharer in ride.sharer_list.all():
        email_receivers.append(sharer.email)
    print("yes") 
    print(email_receivers)   
    email_content = 'Hello, Your ride has been confirmed.\n Ride Info:\n'+\
    'Destination: ' + ride.dest + '\n'+\
    'Arrival time: ' + str(ride.time_arrive) + '\n'+\
    'Driver Name: ' + request.user.username + '\n'+\
    'Vehicle Type: ' + request.user.vehicle.car_type + '\n'
    
    email_sender='1095863872@qq.com'

    send_mail("Ride Confirmed", email_content, email_sender, email_receivers)
    return redirect('driver_search')


@login_required
def complete_ride(request, request_id):
    ride = Ride.objects.filter(pk=request_id)[0]
    ride.status='completed'
    ride.save()
    return redirect('confirmed_display')
    
    
@login_required
def confirmed_display(request):
    confirmed_rides=list(Ride.objects.filter(status = 'confirmed') )

    context = {'confirmed_rides': confirmed_rides}

    if request.method == 'POST':
        request_id = request.POST['request_id']
        return redirect('welcome')
    
    return render(request, 'home/confirmed_display.html', context)
    



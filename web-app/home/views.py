from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import login as auth_login

from django.shortcuts import  render, redirect
from .forms import NewUserForm,VehicleForm,UserProfileUpdateForm

from .models import Vehicle,UserProfile

from django.shortcuts import render,redirect, get_object_or_404


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
    context = {}#context must be dict��  A context is a variable name -> variable value mapping that is passed to a template.
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
    

def welcome(request):
    template = loader.get_template('home/welcome.html')
    context = {}
    return HttpResponse(template.render(context, request))


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
        
    
        # update profile
        #print("where 0")
        print(driverUpdateForm.is_valid())
        #driverUpdateForm1 = VehicleForm(instance=request.user.vehicle)
        #print(driverUpdateForm1.is_valid())
        #if driverUpdateForm.is_valid():
            #print("where 1")
            #profileUpdateForm = UserProfileUpdateForm(instance=request.user)
            
        car_type = driverUpdateForm.cleaned_data.get('car_type')
        capacity = driverUpdateForm.cleaned_data.get('capacity')
            #print("where 2")
            # exception: negative capacity
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



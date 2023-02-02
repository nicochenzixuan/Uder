
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import login as auth_login

from django.shortcuts import  render, redirect
from .forms import NewUserForm


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
    context = {}#context must be dict£¬  A context is a variable name -> variable value mapping that is passed to a template.
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
    
    '''
    template = loader.get_template('home/register.html')
    print("button works?")
    if request.method == 'POST':
        print("yes!")
        username = request.POST['username']
        password = request.POST['password']

        print("print 0")
        user = authenticate(request, username=username)
        if user is None: #can create a new user
            print ("a new user")
            user = User.objects.create_user(
                username = username,
                password = password,
                )
            user.save( )

        else:
            print("")
            print("username exists, please enter a different username")

    context = {}
    return HttpResponse(template.render(context, request))
    '''


def welcome(request):
    template = loader.get_template('home/welcome.html')
    #return HttpResponse("Welcome to our rideapp.")
    context = {}
	  #return render (request=request, template_name="main/register.html", context={"register_form":form})
    return HttpResponse(template.render(context, request))


def driver(request):
    template = loader.get_template('home/driver.html')
    context = {}
    return HttpResponse(template.render(context, request))
  

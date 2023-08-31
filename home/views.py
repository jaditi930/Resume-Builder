from django.shortcuts import redirect,render
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User
from home.models import contact,users_data
from .fetchdata import api_call
import json
import threading

# Create your views here.
def index(request):
    context = {
        "login" : 0
        }
    if request.user.is_authenticated:
        context["login"]=1
        context["user"]=request.user.get_username()
    return render(request,'index.html',context)

def login_user(request):
    return render(request,'login.html')

def login_form(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username,password= password)
        if user is not None:
            login(request,user)
            return redirect ("/")
        else:
            return redirect("/login")

def create_user(request):
    return render(request,"sign_up.html")

def create_user_form(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username,email,password)
        user.first_name=name
        user.save()
        return render(request,'login.html')

def log_out(request):
    logout(request)
    return redirect("/")

def contact_us(request):
    context = {
        "login" : 0
        }
    if request.user.is_authenticated:
        context["login"]=1
        context["user"]=request.user.get_username()
    return render(request,"contact_us.html",context)

def submit_contact_form(request):
    context = {
        "login" : 0
        }
    if request.user.is_authenticated:
        context["login"]=1
        context["user"]=request.user.get_username()

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        temp_contact = contact(name=name,email=email,phone=phone,message=message)
        temp_contact.save()

        return render(request,'contact_us.html',context)

def generate_data(request):
    return render(request,'generate.html')

def generate_data_form(request):
    if request.method == 'POST':
        git = request.POST.get('Github')
        linked = request.POST.get('LinkedIn')
        try:
            temp = users_data.objects.get(f_key=request.user)
        except:
            temp = None
        if temp != None:
            temp.data = ""
            temp.fetch_done = 0
            temp.save()
        else:
            data_entry = users_data(f_key=request.user,fetch_done = 0)
            data_entry.save()
        # print(git)
        # print(linked)
        thread = threading.Thread(target=api_call,args=(git,linked,request))
        thread.start()
        # api_call(git,linked,request)
        return render(request,"generate.html")

def show_resume(request):
    print(request.user.username)
    user_details = {}
    try:
        user=users_data.objects.get(f_key=request.user)
    except:
        user = None

    print(user)
    if user == None:
        user_details["fetch_data_first"] = 1
    else:
        if user.fetch_done == 0:
            user_details["fetch_data_first"] = 0
            user_details["success"] = 0
        else:
            user_details=json.loads(user.data)
            user_details["fetch_data_first"] = 0
            user_details["email"] = request.user.email
            
    print(user_details)
    return render(request,'resume_template.html',context = user_details)

def edit_resume(request):
    # user=users_data.objects.get(f_key=request.user)
    # return render(request,'edit_resume.html',context= {"Data" : user.data})
    user_details = {}
    try:
        user=users_data.objects.get(f_key=request.user)
    except:
        user = None
    if user == None:
        return render(request,'edit_resume.html',context= {"fetch_data_first" : 1})
    else:
        if user.fetch_done == 0:
            return render(request,'edit_resume.html',context= {"fetch_done" : 1})

    return render(request,'edit_resume.html',context= {"Data" : user.data})


def edit_resume_form(request):
    context = {
        "login" : 0
        }
    if request.user.is_authenticated:
        context["login"]=1
        context["user"]=request.user.get_username()

    if request.method == "POST":
        data = request.POST.get('json_string')
        temp = users_data.objects.get(f_key=request.user)
        temp.data = data
        temp.save()
        return render(request,'index.html',context)


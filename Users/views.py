from django.shortcuts import render, redirect
from django.contrib.messages import error
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .middle_drive import hash_pwd, is_valid, get_user
from .models import UserData, User
from User_system import settings
#from django.http import HttpResponse
# Create your views here.

details = {}

def login_(request):
    messages.used = True
    if request.method == "POST":
        username = request.POST.get("username")
        pwd = request.POST.get("pwd")
        if username != None and pwd != None:
            userobject = get_user(username)
            if userobject is not None:
                # print(userobject)
                if username == userobject['email']:
                    if is_valid(userobject.get('password'), pwd):
                        user = authenticate(request, username=userobject['first_name'], password=pwd)
                        if user is not None:
                            nxt = request.POST.get('next')
                            print('redirect to: ' + nxt)
                            login(request, user)
                            if nxt is not None and nxt.startswith('/en') == True:
                                return redirect(str(nxt))
                            else:
                                return redirect('dashboard')
                                
                        else:
                            error(request, "You have no permission for this page")
                            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
                        
    error(request, "wrong username or passwords")
    return render(request, 'Users/login.html')

def register_(request):
    details.clear()
    messages.used = True
    if request.method == "POST":
        fname = request.POST.get("fname")
        if fname == None or fname == '':
            error(request, "first name required")
        mname = request.POST.get("mname")
        if mname == None or fname == '':
            error(request, "valid required!")
        lname = request.POST.get("lname")
        if lname == None or lname == '':
             error(request, "last name required!")
        email = request.POST.get("email")
        if email == None or email == '':
             error(request, "Email required")
        pwd = request.POST.get("pwd")
        c_pwd = request.POST.get("c_pwd")
        if pwd != None or c_pwd != None or pwd != "" or c_pwd !="":
            if pwd != c_pwd:
                error(request, "requires similar passwords")
            else:
                hashed_pwd = hash_pwd(pwd)
                member = UserData(
                    first_name = fname,
                    middle_name = mname,
                    last_name = lname,
                    email = email,
                    password = hashed_pwd
                    )
                member.save()

                user = User.objects.create_user(
                    first_name = fname,
                    last_name = lname,
                    username = fname
                    )
                user.set_password(pwd)
                user.save()
                return redirect('login_')
        else:
            error(request, "Cannot be Empty")
    return render(request, 'Users/register.html')

@login_required
def dashboard(request):
    return render(request, 'Users/dashboard.html', {'details': details})

@login_required
def profile(request, id):
    return render(request, 'Users/profile.html')

def logout_(request):
    logout(request)
    return render (request, "Users/login.html")
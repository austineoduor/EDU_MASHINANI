from django.shortcuts import render, redirect
from django.contrib.messages import error
from django.contrib.auth import login, authenticate
from .middle_drive import hash_pwd, is_valid
#from django.http import HttpResponse
# Create your views here.

details = {}

def login_(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pwd = request.POST.get("pwd")
        if username != None and pwd != None:
            if username == details.get('email'):
                if is_valid(details.get('pwd'), pwd):
                    return redirect('dashboard')
    error(request, "wrong username or passwords")
    return render(request, 'Users/login.html')

def register_(request):
    details.clear()
    if request.method == "POST":
        fname = request.POST.get("fname")
        if fname == None or fname == '':
            error(request, "first name required")
        details['fname'] =fname

        mname = request.POST.get("mname")
        if mname == None or fname == '':
            error(request, "valid required!")
        details["mname"] = mname

        lname = request.POST.get("lname")
        if lname == None or lname == '':
             error(request, "last name required!")
        details["lname"] = lname

        email = request.POST.get("email")
        if email == None or email == '':
             error(request, "Email required")
        details["email"] = email

        pwd = request.POST.get("pwd")
        c_pwd = request.POST.get("c_pwd")
        if pwd != None or c_pwd != None or pwd != "" or c_pwd !="":
            if pwd != c_pwd:
                error(request, "requires similar passwords")
            else:
                hashed_pwd = hash_pwd(pwd)
                details['pwd'] = hashed_pwd
                return redirect('login_')
        else:
            error(request, "Cannot be Empty")
    return render(request, 'Users/register.html')

def dashboard(request):
    return render(request, 'Users/dashboard.html', {'details': details})

def profile(request, id):
    return render(request, 'Users/profile.html')
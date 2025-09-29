from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .middle_drive import hash_pwd, is_valid, get_user
from .models import UserData, User, Course, UserCourse
from django.conf import settings
#from django.http import HttpResponse
# Create your views here.

def login_(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            nxt = request.POST.get('next')
            if nxt and nxt.startswith('/en'):
                return redirect(str(nxt))
            return redirect(settings.LOGIN_REDIRECT_URL)      
        else:
            messages.error(request, "Invalid Email/Username or password")
            return redirect(f"{settings.LOGIN_URL}?next={request.path}") 
                        
    return render(request, 'index.html', {"show_register": False})

def register_(request):
    if request.method == "POST":

        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        pwd1 = request.POST.get("password1")
        pwd2 = request.POST.get("password2")

        if not first_name or not last_name or not email:
            messages.error(request, "First name, last name, and email are required")
            # return render(request, "index.html", {"show_register": True})

        elif pwd1 != pwd2:
            messages.error(request, "Passwords do not match")
            # return render(request, "index.html",  {"show_register": True})
        

        # Create Django User (use email as username for uniqueness)
        elif User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            # return render(request, "index.html",  {"show_register": True})
        
        # Save in custom UserData with bcrypt hash
        else:
            member = User.objects.create_user(
                username=email,
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = pwd1
                )
         # Create linked UserData
        UserData.objects.create(
            user=member,
            middle_name=middle_name
        )
        
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login_")
    
    return render(request, 'index.html', {"show_register": True})

@login_required
def dashboard(request):
    user = request.user
    user_data = getattr(user, "userdata", None)
    courses = Course.objects.all()
    user_courses = UserCourse.objects.filter(user=request.user)

    applied_courses_ids = user_courses.values_list("course_id", flat=True)
    context = {
        
        "user": user,
        "user_data": user_data,
        "courses": courses,
        "user_courses": user_courses,
        "applied_courses_ids": applied_courses_ids,
    }
    return render(request, 'Users/dashboard.html', context)

@login_required
def apply_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    user_course, created = UserCourse.objects.get_or_create(
        user=request.user, course=course
    )
    if created:
        messages.success(request, f"You have successfully applied for {course.name}")
    else:
        messages.info(request, f"You already applied for {course.name}")

    return redirect("dashboard")

@login_required
def profile(request, id):
    return render(request, 'Users/profile.html')

def logout_(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
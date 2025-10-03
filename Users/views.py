from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# from .forms import CourseApplicationForm
# from .middle_drive import hash_pwd, is_valid, get_user
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
            messages.error(request, "Invalid Email/Username or password", extra_tags='login')
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
            messages.error(request, "First name, last name, and email are required", extra_tags='register')
            # return render(request, "index.html", {"show_register": True})

        elif pwd1 != pwd2:
            messages.error(request, "Passwords do not match", extra_tags='register')
            # return render(request, "index.html",  {"show_register": True})
        

        # Create Django User (use email as username for uniqueness)
        elif User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered", extra_tags='register')
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
        
        messages.success(request, "Account created successfully. Please log in.", extra_tags='register')
        return redirect("login_")
    
    return render(request, 'index.html', {"show_register": True})

@login_required
def dashboard(request):
    user = request.user
    # user_data = getattr(user, "userdata", None)
    courses = Course.objects.all()
    user_courses = UserCourse.objects.filter(user=request.user)

    applied_courses_ids = user_courses.values_list("course_id", flat=True).exclude(status=UserCourse.STATUS_NOT_APPLIED)

    context = {
        
        # "user": user,
        #  "user_data": user_data,
        "courses": courses,
        # "user_courses": user_courses,
        "applied_courses_ids": applied_courses_ids,
    }
    return render(request, 'Users/dashboard.html', context)

@login_required
def profile(request, id):
    """
    Show the profile page for the logged-in user.
    If 'id' is provided, show that user's profile instead.
    """
    
    if request.user.id != id:
        raise Http404("profile not found") 

    user = request.user
    # Get user's courses
    user_courses = UserCourse.objects.filter(user=user).select_related("course")
    # user_data = getattr(user, "profile", None)
    context = {
        "user": user,
        # "user_data": user_data,
        "courses": user_courses,
    }
    return render(request, "Users/profile.html", context)

@login_required
def apply_course(request, course_id):
    
    course = get_object_or_404(Course, id=course_id)

    # Check if the user has already applied for this course
    user_course = UserCourse.objects.filter(user=request.user, course=course).first()

    # If user already applied or is in progress/completed, block new applications
    if user_course and user_course.status in [
        UserCourse.STATUS_APPLIED,
        UserCourse.STATUS_IN_PROGRESS,
        UserCourse.STATUS_COMPLETED,
    ]:
        messages.info(request, "You have already applied or are currently enrolled in this course.")
        return redirect("dashboard")

    # If no record exists, create one but don't save yet
    if not user_course:
        user_course = UserCourse(user=request.user, course=course)

    if request.method == "POST":
        # Checkbox validations
        has_stable_power = request.POST.get('has_stable_power') == 'on'
        has_laptop = request.POST.get('has_laptop') == 'on'
        agrees_to_terms = request.POST.get('agree_to_terms') == 'on'

        location = request.POST.get("location")
        about = request.POST.get("about")

        if not (has_stable_power and has_laptop and agrees_to_terms):
            messages.error(request, "You must confirm all fields to apply.")
        elif not location or not about:
            messages.error(request, "Provide both location and about details.")
        else:
            # Update profile
            user_profile = request.user.profile
            user_profile.location = location
            user_profile.about = about
            user_profile.save()

            # Save course application
            user_course.status = UserCourse.STATUS_APPLIED
            user_course.save()

            messages.success(request, f"You have successfully applied for {course.name}")
            return redirect("dashboard")

    # GET request or validation error → show form
    context = {
        "course": course,
        "user_course": user_course,
    }
    return render(request, "Users/apply_course.html", context)
    
def logout_(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
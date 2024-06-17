from django.urls import path

from . import views
# app_name = "Users"
urlpatterns = [
        path("", views.register_, name="register_"),
        path("register/", views.register_, name="register_"),
        path("login/", views.login_, name="login_"),
        path("dashboad/", views.dashboard, name="dashboard"),
        path("<int:id>/profile/", views.profile, name="profile"),
]

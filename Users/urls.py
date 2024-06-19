from django.urls import path

from . import views
# app_name = "Users"
urlpatterns = [
        path("", views.login_, name="login_"),
        path("register/", views.register_, name="register_"),
        path("login/", views.login_, name="login_"),
        path("logout/", views.logout_, name="logout_"),
        path("dashboard/", views.dashboard, name="dashboard"),
        path("<int:id>/profile/", views.profile, name="profile"),
]

from django.urls import path

from . import views
# app_name = "Users"
urlpatterns = [
        path("register/", views.register_, name="register_"),
        path("login/", views.login_, name="login_"),
        path("logout/", views.logout_, name="logout_"),
        path("dashboard/", views.dashboard, name="dashboard"),
        path("<int:id>/profile/", views.profile, name="profile"),
        path("profile/<int:user_id>/edit/", views.edit_profile, name="edit_profile"),
        path("course/apply/<int:course_id>/", views.apply_course, name="apply_course"),
        path('courses/<int:course_id>/content/', views.course_content, name='course_content'),
]

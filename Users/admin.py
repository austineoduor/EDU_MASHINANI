from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import path
from django.template.response import TemplateResponse

from .models import User, UserData, Course, UserCourse


# -----------------------------
# Inline for user profile editing
# -----------------------------
class UserDataInline(admin.StackedInline):
    model = UserData
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"


# -----------------------------
# Custom User Admin
# -----------------------------
class CustomUserAdmin(UserAdmin):
    inlines = [UserDataInline]
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


# -----------------------------
# Inline for showing user enrollments in course admin
# -----------------------------
class UserCourseInline(admin.TabularInline):
    model = UserCourse
    extra = 0
    fields = ("user", "status", "score", "applied_at")
    readonly_fields = ("user", "applied_at")
    show_change_link = True


# -----------------------------
# Course Admin
# -----------------------------
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "created_at")
    search_fields = ("name", "category")
    inlines = [UserCourseInline]
    ordering = ("name",)
    date_hierarchy = "created_at"


# -----------------------------
# User Course Admin (with color-coded status & actions)
# -----------------------------
@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "colored_status", "score", "applied_at", "modified_at")
    search_fields = ("user__username", "course__name")
    readonly_fields = ("user", "course", "applied_at")
    list_filter = ("status", "course")
    list_select_related = ("user", "course")
    ordering = ("-applied_at",)
    date_hierarchy = "applied_at"
    actions = ["mark_completed", "mark_in_progress"]

    def colored_status(self, obj):
        colors = {
            "not_applied": "gray",
            "applied": "blue",
            "in_progress": "orange",
            "completed": "green",
        }
        return format_html(
            '<b style="color:{};">{}</b>',
            colors.get(obj.status, "black"),
            obj.get_status_display()
        )
    colored_status.short_description = "Status"

    def mark_completed(self, request, queryset):
        count = queryset.update(status=UserCourse.STATUS_COMPLETED)
        self.message_user(request, f"{count} user courses marked as Completed.")
    mark_completed.short_description = "Mark selected as Completed"

    def mark_in_progress(self, request, queryset):
        count = queryset.update(status=UserCourse.STATUS_IN_PROGRESS)
        self.message_user(request, f"{count} user courses marked as In Progress.")
    mark_in_progress.short_description = "Mark selected as In Progress"


# -----------------------------
# User Data Admin
# -----------------------------
@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ("user", "location", "created_at", "updated_at")
    search_fields = ("user__username", "location")
    ordering = ("-created_at",)


# -----------------------------
# Optional: Custom Dashboard
# -----------------------------
def admin_dashboard_view(request):
    context = dict(
        admin.site.each_context(request),
        user_count=User.objects.count(),
        course_count=Course.objects.count(),
        active_enrollments=UserCourse.objects.filter(status="in_progress").count(),
        completed_courses=UserCourse.objects.filter(status="completed").count(),
    )
    return TemplateResponse(request, "admin/dashboard.html", context)

# Inject custom URLs into the default admin
def get_admin_urls(urls):
    def wrapper():
        return [
            path('dashboard/', admin.site.admin_view(admin_dashboard_view), name='dashboard'),
            *urls(),
        ]
    return wrapper

admin.site.get_urls = get_admin_urls(admin.site.get_urls)

# -----------------------------
# Final admin registration
# -----------------------------
# admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
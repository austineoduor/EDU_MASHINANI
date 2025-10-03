from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserData, UserCourse, Course
from .models import UserCourse

admin.site.register(User, UserAdmin)
admin.site.register(UserData)
admin.site.register(UserCourse)
admin.site.register(Course)


class CourseInline(admin.TabularInline):
    model = UserCourse
    extra = 0  # Number of empty forms to show

class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseInline]  # Add the inline model for related `UserCourse`


class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status')
    search_fields = ('user__username', 'course__name')
    readonly_fields = ("user", "course", "applied_at")  # Make user and course read-only in the admin
    list_filter = ('status', 'course')
    ordering = ('-status',)  # Order by status (descending)
    

    fieldsets = (
        (None, {
            'fields': ('user', 'course', 'status'),
        }),
        ('Advanced Options', {
            'classes': ('collapse',),
            'fields': ('date_applied',),  # Optional: Add extra fields if needed
        }),
    )



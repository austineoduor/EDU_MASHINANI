"""
Improved Django models for your project.
- Includes: clearer related_name usage, helper methods, validators, and a post_save signal
  to ensure a profile is created for each User.
- Migration-safe notes included as comments at the bottom.

Filename note: your original file was named `modes.py` — standard Django expects `models.py`.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import json


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser.

    Keeping a custom user model allows you to add fields later without changing
    AUTH_USER_MODEL in the middle of a project.
    """

    def get_profile(self):
        """Return the related UserData instance, creating it if missing.

        Use this helper in views/templates to avoid AttributeError when a profile
        hasn't been created yet.
        """
        profile, _ = UserData.objects.get_or_create(user=self)
        return profile


class UserData(models.Model):
    """Extended user profile information.

    Note: related_name is set to 'profile' so you can access it with `user.profile`
    (if it exists). Use `user.get_profile()` to ensure a profile object exists.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s profile"


class Course(models.Model):
    """Available courses for users to register.

    components and applications are stored as `TextField` for backwards
    compatibility with your existing data. Helper methods try to parse JSON
    or fallback to comma-separated parsing.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    components = models.TextField(blank=True, null=True)
    applications = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def _parse_text_field(self, value):
        """Try to parse a field that's either JSON (list) or comma-separated text.

        Returns a list of strings (trimmed) or an empty list.
        """
        if not value:
            return []

        # Try JSON first (useful if you migrate to JSONField later)
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return [str(x).strip() for x in parsed]
        except Exception:
            pass

        # Fallback: comma-separated
        return [part.strip() for part in value.split(",") if part.strip()]

    def get_components(self):
        return self._parse_text_field(self.components)

    def get_applications(self):
        return self._parse_text_field(self.applications)


class UserCourse(models.Model):
    """Mapping of users to courses with status & progress tracking."""
    STATUS_APPLIED = "applied"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = [
        (STATUS_APPLIED, "Applied"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_COMPLETED, "Completed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="students")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_APPLIED)
    # Score is constrained between 0 and 100; change validators if you use a different scale
    score = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")
        ordering = ["course__name"]

    def __str__(self):
        return f"{self.user.username} → {self.course.name} ({self.status})"


# ------------------ Signals ------------------
@receiver(post_save, sender=User)
def ensure_user_profile(sender, instance, created, **kwargs):
    """Ensure a UserData/profile is created when a new User is created.

    This is helpful so templates can safely access `user.profile` after user
    creation; alternatively use `user.get_profile()` where appropriate.
    """
    if created:
        UserData.objects.get_or_create(user=instance)
        
from django import forms
from .models import UserCourse

class CourseApplicationForm(forms.ModelForm):
    class Meta:
        model = UserCourse
        fields = ['course', 'status', 'has_stable_power', 'has_laptop', 'agree_to_terms', 'location', 'about']

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status == UserCourse.STATUS_APPLIED:
            raise forms.ValidationError("You cannot set the status to 'applied' manually.")
        return status
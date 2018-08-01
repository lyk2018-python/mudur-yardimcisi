from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from muduryardimci.models import Courses

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("course_id","email")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email= self.cleaned_data["email"]
        if commit:
            user.save()
        return user
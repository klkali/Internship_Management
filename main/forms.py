from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Internship, Application

class UserRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = ['title', 'description', 'requirements', 'location', 'stipend']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'email', 'resume']


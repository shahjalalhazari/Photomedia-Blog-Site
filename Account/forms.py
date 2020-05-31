from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from . import models


# SIGNUP FORM
class SignupForm(UserCreationForm):
    first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Username'}))
    email = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Email Address'}))
    password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


# SIGNIN/LOGIN FORM
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':"Username"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    class Meta:
        model = User
        fields = ['username', 'password']


# PROFILE INFO CHANGE FORM
class ProfileInfoChange(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


# PROFILE PHOTO CHANGE FORM
class ProfilePic(forms.ModelForm):
    class Meta:
        model = models.ProfilePhoto
        fields = ['profile_pic']
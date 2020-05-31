from django.shortcuts import render, HttpResponseRedirect, Http404, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse

from . import models, forms


# SIGNUP VIEW
def signup(request):
    form = forms.SignupForm()
    register = False
    if request.method == "POST":
        form = forms.SignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            register = True
    return render(request, 'Account/signup.html', {'form':form, 'register':register})


# LOGIN VIEW
def user_login(request):
    form = forms.LoginForm()
    if request.method == "POST":
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('blog:index'))
    return render(request, 'Account/login.html', {'form':form})


# LOGOUT VIEW
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:index'))


# PROFILE VIEW
class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'Account/profile.html'


# PROFILE INFO CHANGE VIEW
@login_required
def edit_profile(request):
    changed = False
    current_user = request.user
    form = forms.ProfileInfoChange(instance=current_user)
    if request.method == "POST":
        form = forms.ProfileInfoChange(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            changed = True
    return render(request, 'Account/edit_profile.html', {'form':form, 'changed':changed})


# PASSWORD CHANGE VIEW
@login_required
def edit_password(request):
    changed = False
    current_user = request.user
    form = PasswordChangeForm(current_user)
    if request.method == "POST":
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            changed = True
    return render(request, 'Account/edit_password.html', {'form':form, 'changed':changed})


# ADD PROFILE PHOTO
@login_required
def add_photo(request):
    form = forms.ProfilePic()
    changed = False
    if request.method == "POST":
        form = forms.ProfilePic(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            changed = True
    return render(request, 'Account/profile_photo.html', {'form':form, 'changed':changed})


# CHANGE PROFILE PHOTO
@login_required
def change_photo(request):
    form = forms.ProfilePic(instance=request.user.user_profile)
    changed = False
    if request.method == "POST":
        form = forms.ProfilePic(request.POST, request.FILES, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            changed= True
    return render(request, 'Account/profile_photo.html', {'form':form, 'changed':changed})


# OTHER USER PROFILE VIEW
def other_user(request, username):
    other_user = models.User.objects.get(username=username)
    if request.user.is_authenticated and request.user == other_user:
        return HttpResponseRedirect(reverse('account:profile'))
    else:
        return render(request, 'Account/user.html', {'other_user':other_user,})
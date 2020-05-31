from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    #path('profile/<username>/', views.profile, name='profile'),
    path('', views.Profile.as_view(), name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('password/', views.edit_password, name='password'),
    path('add-photo/', views.add_photo, name='add_photo'),
    path('change-photo/', views.change_photo, name='change_photo'),
    path('<username>/', views.other_user, name='other_user'),
]
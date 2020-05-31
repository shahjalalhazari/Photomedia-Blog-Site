from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.index, name='index'),
    path('write/', views.WriteBlog.as_view(), name='write'),
    path('blogs/', views.BlogList.as_view(), name='blogs'),
    path('create-category/', views.CreateCategory.as_view(), name='create_category'),
    path('blog/<slug:slug>/', views.full_blog, name='full_blog'),
    path('like/<pk>/', views.like, name='like'),
    path('unlike/<pk>/', views.unlike, name='unlike'),
    path('categories/', views.category_list, name='categories'),
    path('category/<int:cat_id>/', views.category, name='category'),
    path('edit-blog/<slug>/', views.EditBlog.as_view(), name='edit_blog'),
    path('delete-blog/<slug>/', views.DeleteBlog.as_view(), name='delete_blog'),
]
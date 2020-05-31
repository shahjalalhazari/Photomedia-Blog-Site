from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Blog.urls')),
    path('account/', include('Account.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()
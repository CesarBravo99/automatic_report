"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from easy_label.views.download import download
from easy_label.views.easy_label import easy_label
from easy_label.views.home import home
from easy_label.views.tutorial import tutorial
from easy_label.views.upload_images import upload_images

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('tutorial', tutorial, name='tutorial'),
    path('upload-images', upload_images, name='upload-images'),
    path('<int:images_dir>', easy_label, name='easy-label'),
    path('json-download', download, name='download'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

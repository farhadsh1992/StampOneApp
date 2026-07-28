"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
#######################################################
from django.contrib import admin
from django.urls import path
from django.urls import include

#######################################################
## I added
from django.conf import settings
from django.conf.urls.static import static 


from . import views
from . import models
from FarhadCV.Tools import tcolors, bcolors
#######################################################

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.splash, name='splash'),
    path('decode/', views.index, name='home'),
    path('index.html', models.selector_detector, name='home2'),
    # path('about/', views.about),
    # path('posts/', include('post.urls'))
]


#######################################################
######                                       ######
#######################################################
## allow us to set our url that we need it 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.IMAGES_URL, document_root=settings.IMAGES_ROOT)
    urlpatterns += static(settings.ENC_URL, document_root=settings.ENC_ROOT)
    urlpatterns += static(settings.FACE_URL, document_root=settings.FACE_ROOT)


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
from django.urls import path, re_path
from django.urls import include

#######################################################
## I added
from django.conf import settings
from django.views.static import serve


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
## Serve uploaded/decoded images directly via django.views.static.serve.
## django.conf.urls.static.static() looks like the "normal" way to do this, but
## it silently no-ops whenever settings.DEBUG is False - and DEBUG is False in
## production here, with no separate media server/CDN configured (whitenoise
## only covers STATIC_URL, not these). Wiring `serve` directly bypasses that
## DEBUG gate - a pragmatic choice for a small single-instance app.
urlpatterns += [
    re_path(r"^media/Encoded_images/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^media/Encoded_faces/(?P<path>.*)$", serve, {"document_root": settings.FACE_ROOT}),
    re_path(r"^Images/(?P<path>.*)$", serve, {"document_root": settings.IMAGES_ROOT}),
]


"""djangoexplore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include

from django.views.generic import TemplateView
from cartographer.views import cartographer

from core.views import signup

from api.views import UserViewSet#, create_auth
from api.router import router as apiRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", cartographer, name = "conflictcartographer"),
    path("api/",include(apiRouter.urls)),
    path("invitations/",include("invitations.urls",namespace = "invitations")),
    path("accounts/",include("django.contrib.auth.urls")),
    path("accounts/signup",signup,name = "signup"),
    #path("reg/", create_auth)
]


from django.urls import path, include
from .views import signup, bulkAdd

urlpatterns =[
    path("accounts/",include("django.contrib.auth.urls")),
    path("accounts/signup",signup,name = "signup"),
    path("accounts/bulkadd/",bulkAdd,name="bulkadd"),
]

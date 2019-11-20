
from django.urls import path, include
from django.conf.urls import url
from .views import signup, bulkAdd, referralRedirect, referralSignup 

urlpatterns =[
    path("accounts/",include("django.contrib.auth.urls")),
    url("accounts/ref/(?P<refkey>[^/.]+)/$",referralRedirect, name="referral"),
    url("accounts/signup",referralSignup, name="referralSignup"),
    #path("accounts/signup",signup,name = "signup"),
    path("accounts/bulkadd/",bulkAdd,name="bulkadd"),
]

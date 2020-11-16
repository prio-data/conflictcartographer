
from django.urls import path, include
from rest_framework.urls import path
from rest_framework import routers

from api.views import *

router = routers.DefaultRouter()

router.register(r"shapes",ShapeViewSet)
router.register(r"countries",CountryViewSet)

urlpatterns = [
    path("api/assigned/", projects),
    path("api/",include(router.urls)),
    path("api/updatecountries/",updateCountries,name="updatecountries"),
    path("api/whoami/",whoami),
    path("api/currentproject/",projectInfo),
    path("api/waiver/",waiver),
    path("accounts/profile/",editProfile),
    path("api/hasprofile/",hasProfile),
    path("api/projectchoices/",projectChoices),
    path("api/editprojects/<str:action>/",editProjects),
    #path("api/pinfo/completed/<int:pk>/",completedProject),
    path("api/calendar/",calendar),
    path("api/nonanswer/<int:project>/",nonanswer),
    path("api/projectstatus/<int:project>/",projectStatus),
    path("api/clearshapes/<int:project>/",clearShapes),
]


from django.urls import path, include
from rest_framework.urls import path
from rest_framework import routers

from api.views import *

router = routers.DefaultRouter()

router.register(r"shapes",ShapeViewSet,basename="shape")
router.register(r"countries",CountryViewSet,basename="country")
router.register(r"feedback",FeedbackViewset,basename="feedback")

urlpatterns = [
    path("api/assigned/", projects,name="assigned"),
    path("api/",include(router.urls)),
    path("api/updatecountries/",updateCountries,name="updatecountries"),
    path("api/whoami/",whoami,name="whoami"),
    path("api/currentproject/",projectInfo),
    path("api/waiver/",waiver),
    path("accounts/profile/",editProfile),
    path("api/hasprofile/",hasProfile),
    path("api/projectchoices/",projectChoices),
    path("api/editprojects/<str:action>/",editProjects),
    #path("api/pinfo/completed/<int:pk>/",completedProject),
    path("api/calendar/",calendar),
    path("api/nonanswer/<int:project>/",nonanswer,name="nonanswer"),
    path("api/projectstatus/<int:project>/",projectStatus,name="projectstatus"),
    path("api/clearshapes/<int:project>/",clearShapes),
]

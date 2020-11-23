
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

    path("api/currentproject/",projectInfo,name="projecttext"),
    path("api/waiver/",waiver,name="waivetext"),
    path("api/calendar/",calendar,name="timestatus"),

    path("api/whoami/",whoami,name="whoami"),

    path("accounts/profile/",editProfile,name="editprofiledata"),
    path("api/hasprofile/",hasProfile,name="hasprofiledata"),

    path("api/projectchoices/",projectChoices,name="countrychoices"),
    path("api/editprojects/<str:action>/",editProjects,name="selectcountries"),

    path("api/nonanswer/<int:project>/",nonanswer,name="nonanswer"),
    path("api/projectstatus/<int:project>/",projectStatus,name="projectstatus"),
    path("api/clearshapes/<int:project>/",clearShapes,name="clearshapes"),
]

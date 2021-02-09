
from django.urls import path, include
from rest_framework.urls import path
from rest_framework import routers

from api.views import *

router = routers.DefaultRouter()

router.register(r"shapes",ShapeViewSet,basename="shape")
router.register(r"countries",CountryViewSet,basename="country")
router.register(r"feedback",FeedbackViewset,basename="feedback")

urlpatterns = [
    path("api/",include(router.urls)),
    path("api/updatecountries/",updateCountries,name="updatecountries"),

    path("api/currentproject/",projectInfo,name="projecttext"),
    path("api/waiver/",waiver,name="waivetext"),
    path("api/calendar/",calendar,name="timestatus"),

    path("api/whoami/",whoami,name="whoami"),

    path("api/projectchoices/",projectChoices,name="countrychoices"),
    path("api/editprojects/<str:action>/",editProjects,name="selectcountries"),

    path("api/nonanswer/<int:project>/",nonanswer,name="nonanswer"),
    path("api/projectstatus/<int:project>/",projectStatus,name="projectstatus"),
    path("api/clearshapes/<int:project>/",clearShapes,name="clearshapes"),

    # Project status
    path("api/assigned/", projects,name="assigned"),
    path("api/unfulfilled/",unfulfilled,name="unfulfilled"),

    # Metadata entry
    path("accounts/profile/",editProfile,name="editprofiledata"),

    path("api/profile_meta/",profile_meta,name="profile_meta"),
    path("api/hasprofile/",hasProfile,name="hasprofiledata"),
    path("api/questions/",unfulfilled,name="unfulfilled"),

    # Current project info
    path("api/info/short/",lambda rq: projectInfo(rq),name="current_info"),
    path("api/info/verbose/",lambda rq: projectInfo(rq,verbose=True),name="current_info_verbose"),

    path("api/period/current/",get_quarter,name="current_span"),
    path("api/period/next/",lambda rq: get_quarter(rq,shift=1),name="next_span"),
    path("api/period/previous/",lambda rq: get_quarter(rq,shift=-1),name="previous_span"),
    
    # Profile info
    path("api/profile/meta/",profile_meta,name="profile_meta_detail"),
    path("api/profile/exists/",hasProfile,name="profile_meta_exists"),

    path("api/profile/assigned/",projects,name="assigned_list"),
    path("api/profile/unfulfilled/",unfulfilled,name="unfulfilled_list"),
    path("api/profile/next/",next_project,name="next_project"),

    path("api/profile/pending/",pending_projects,name="unfulfilled_list"),
    path("api/profile/fulfilled/",fulfilled_projects,name="unfulfilled_list"),

    # Projects
    path("api/projects/",projectChoices)
]

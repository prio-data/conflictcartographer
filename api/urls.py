
from api.views import profile 
from django.urls import path 
from rest_framework.urls import url

urlpatterns = [
    # Pk is passed as a query, even though it is a path?
    # Magical!
    url("api/profile/(?P<pk>[^/.]+)/$", profile)

]

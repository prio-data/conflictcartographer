
from rest_framework import permissions
from django.urls import resolve
from django.utils import timezone
from api import models, util, serializers
from datetime import datetime

import logging

logger = logging.getLogger(__name__)

# ================================================
# Util

def breachLog(request,msg):
    HEADER = "\x1b[38;5;196m[PERMBREACH]\x1b[0m "
    logger.error(HEADER + f"<{request.user.username}> " + msg)

def justUrl(url):
    return url.split("?")[0]

# ================================================
# Permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Only owner can delete shapes
    """

    def has_object_permission(self,request,view,obj):

        # View methods (GET HEAD OPTIONS) 
        allowed = request.method in permissions.SAFE_METHODS

        # Is owner or superuser
        allowed |= (obj.author == request.user) | request.user.is_staff
        if not allowed:
            breachLog(request,f"tried altering {obj.author}'s shape.")


        return allowed

class IsOnProject(permissions.BasePermission):
    """
    Only allows posting data to a project if a user is part of that project.
    """

    def has_permission(self, request, view):
        allowed = True 

        if request.method == "POST":
            userProjects = request.user.projects.all()
            targetProject = justUrl(request.data["project"])

            for p in userProjects:
                projectUrl = util.getUrl(p, serializers.ProjectSerializer, request)
                allowed |= targetProject == projectUrl 

            if not allowed:
                projname = request.data["project"]
                breachLog(request,f"not participant to {projname}!")

        return allowed

class ProjectIsActive(permissions.BasePermission):
    """
    Restricts non-admin users from posting to non-active projects.
    """

    def has_permission(self, request, view):
        now = datetime.now(timezone.get_current_timezone())

        # GETs only return active projects anyway...
        allowed = True 
    
        if request.method == "POST":
            userProjects = request.user.projects.all()
            targetProject = justUrl(request.data["project"])

            # Finding the current project
            for p in userProjects:

                projectUrl = util.getUrl(p, serializers.ProjectSerializer, request)
                if projectUrl == targetProject:
                    postingTo = p
                    break

                else:
                    postingTo = None

            # Check if project has ended

            if postingTo is not None:
                allowed &= postingTo.startdate < now
                allowed &= postingTo.enddate > now

                if not allowed:
                    breachLog(request,f"{targetProject} is not active!")

            else:
                allowed = False
                    
        return allowed

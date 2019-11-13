
from rest_framework import permissions, exceptions
from django.urls import resolve
from django.utils import timezone
from api import models, util, serializers
from datetime import datetime

import logging

import re

logger = logging.getLogger(__name__)

# ================================================
# Util

def breachLog(request,msg):
    HEADER = "\x1b[38;5;196m[PERMBREACH]\x1b[0m "
    logger.error(HEADER + f"<{request.user.username}> " + msg)

def getProjectPkFromUrl(url):
    """
    Returns the only //-enclosed number in the URL.
    Probably always the PK of the object, right?

    Very important to get right for comparisons!
    """

    def numberpath(url):
        m = re.search("(?<=/)[0-9]+(?=/)", url)
        if m:
            return int(m[0])
        else:
            raise exceptions.ParseError

    without_params = lambda x: x.split("?")[0]
    without_protocol = lambda x: x.split("//")[1]

    return numberpath(without_params(without_protocol(url)))
    

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
        allowed = request.user.is_staff

        if request.method == "POST":
            targetProject = getProjectPkFromUrl(request.data["project"])

            userProjects = request.user.projects.all()
            for p in userProjects:
                allowed |= targetProject == p.pk 

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
            targetProject = getProjectPkFromUrl(request.data["project"])

            # Finding the current project
            userProjects = request.user.projects.all()
            for p in userProjects:

                if p.pk == targetProject:
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

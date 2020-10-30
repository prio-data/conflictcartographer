
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

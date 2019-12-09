from django.db import models

from django.conf import settings

from django.contrib.auth.models import User
from api.models import Project

from core.util import hasDrawn, referralKeygen

from django.core import mail 
from django.template.loader import render_to_string

from datetime import datetime
from hashlib import md5

import names

class Cohort(models.Model):
    stamp = models.CharField(
       max_length = 10, 
       unique = True)

    name = models.CharField(
       max_length = 100,
       default = names.get_full_name)

    created = models.DateField(auto_now = True)

    def dispatch(self):
        todo = [i for i in self.invitations.all() if not i.taskAccomplished()]
        for invitation in todo:
            invitation.dispatch()

    def __str__(self):
        return f"Cohort \"{self.name}\" ({self.stamp}) {len(self.invitations.all())} invitation(s)"


class Invitation(models.Model):

    email = models.EmailField(unique = True)

    # These projects are added to user upon registration
    projects = models.ManyToManyField(Project,
        related_name = "projects")

    # Grouping together batches of invitations
    cohort = models.ForeignKey(Cohort,
        related_name = "invitations", null = True, blank = True,
        on_delete = models.CASCADE)
        
    # Added when user completes registration
    user = models.OneToOneField(
        User, related_name = "invitation", null = True, blank = True,
        on_delete = models.CASCADE)

    refkey = models.CharField(max_length = 32, unique = True)

    # View tags
    # These are altered by the invited user going to views, registering, etc.
    reached = models.BooleanField(default = False) # Did the email arrive
    opened = models.BooleanField(default = False) # Did the invited user go to the link 
    registered = models.BooleanField(default = False) # Did the invited user register

    @classmethod
    def create(cls, email, projects, cohort = None):
        """
        Create an invite from email and a list of projects
        """
        projects = Project.objects.filter(pk__in = projects)
        refkey = referralKeygen(email)
        
        i = cls(email = email, refkey = refkey, cohort = cohort)
        i.save()
        i.projects.set(projects)

        return i

    def dispatch(self):
        """
        Sends the invitation with a message which is cased depending on what
        the user has done so far. 
        """

        link = settings.INVITATION_LINK_BASE.format(key = self.refkey)

        title = self.caseTitle()

        emails = [
            ("plain",settings.PLAINTEXT_MAIL_TEMPLATE),
            ("html",settings.HTML_MAIL_TEMPLATE)]

        templateValues = {"link":link,"status":self.invitation_status()}
        emails = {k:render_to_string(template,templateValues) 
            for k,template in emails}

        try:
            res = mail.send_mail(title,
                emails["plain"],
                settings.EMAIL_FROM_ADDRESS,
                [self.email],
                html_message = emails["html"])

        except ConnectionRefusedError:
            return False

        else:
            self.reached = True
            self.save()
            return True

    def caseTitle(self):
        """
        Adapts the message-portion of the invitation email,
        based on what the invitee has so far done.
        """
        title = "Invitation to participate in a geo-spatial expert survey"
        if self.invitation_status() == "...":
            title = "REMINDER: " + title
        return title


        return title, msg

    def taskAccomplished(self):
        """
        Used to prevent dispatch if user has drawn something
        """

        if self.user is not None:
            return hasDrawn(self.user)

        else:
            return False

    def invitation_status(self): # "Tagged" by various views
        if self.user is not None:
            if hasDrawn(self.user):
                status = "drawn"
            else:
                status = "registered"
        elif self.opened:
            status = "opened"
        elif self.reached:
            status = "reached"
        else:
            status = "..."
        return status

    def __str__(self):
        return f"Invitation for {self.email} ({self.invitation_status()})"

def makeStamp(x):
    return "abc"
    

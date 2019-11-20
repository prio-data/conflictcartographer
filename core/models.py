from django.db import models

from django.contrib.auth.models import User
from api.models import Project

from datetime import datetime
from hashlib import md5

def makeStamp():
    return md5(str(datetime.now().date()).encode()).hexdigest()[0:10]
    
class Cohort(models.Model):
   stamp = models.CharField(
      max_length = 10, 
      unique = True,
      default = makeStamp)

class Invitation(models.Model):
    refkey = models.CharField(max_length = 32, unique = True) # Should be a hashed version of something

    email = models.EmailField()
    projects = models.ManyToManyField(Project,
        related_name = "projects")

    # Useful for grouping together batches of invitations
    cohort = models.ForeignKey(Cohort,
        related_name = "invitations", null = True, blank = True,
        on_delete = models.CASCADE)
        
    # Added when user completes registration
    user = models.OneToOneField(
        User, related_name = "invitation", null = True, blank = True,
        on_delete = models.CASCADE)

    reached = models.BooleanField(default = False) # Did the email arrive
    opened = models.BooleanField(default = False) # Did the invited user go to the link 
    registered = models.BooleanField(default = False) # Did the invited user register

    def invitation_status(self):
        if self.registered:
            status = "registered"
        elif self.opened:
            status = "opened"
        elif self.reached:
            status = "reached"
        else:
            status = "failed"
        return status

    def __str__(self):
        return f"Invitation for {self.email} ({self.invitation_status()})"

import os
from typing import List

import logging

from pydantic import BaseModel,EmailStr,constr

from django.conf import settings

from django.db.models import CharField,Model,OneToOneField,ManyToManyField
from django.db.models import BooleanField,JSONField,EmailField,CASCADE

from django.contrib.auth.models import User

from django.core import mail 
from django.template.loader import render_to_string
from django.db.utils import IntegrityError

from api.models import Country,Profile

from invitations.util import referralKeygen

logger = logging.getLogger(__name__)

class Invitation(Model):
    """
    The invitation class
    """
    email = EmailField(unique = True)
        
    # Added when user completes registration
    user = OneToOneField(
        User, related_name = "invitation", null = True, blank = True,
        on_delete = CASCADE)

    mailed = BooleanField(default=False)
    metadata = JSONField(default=dict,blank=True)

    countries = ManyToManyField(Country,related_name="invited_assignees")

    refkey = CharField(max_length = 32, null = True)


    def makeProfile(self,user):
        profile = Profile(
            meta = self.metadata,
            user = user
        )
        profile.save()
        profile.countries.set(self.countries.all())
        return profile

    def invitationLink(self):
        return os.path.join(settings.INVITATION_LINK_BASE,self.refkey)

    def dispatch(self):
        """
        Sends the invitation by email 
        """

        if self.refkey is None:
            self.refkey = referralKeygen(self.email)
            self.save()

        title = settings.EMAIL_TITLE 

        emails = [
            ("plain",settings.PLAINTEXT_MAIL_TEMPLATE),
            ("html",settings.HTML_MAIL_TEMPLATE)]

        emails = {k:render_to_string(template,{"link":self.invitationLink()})
            for k,template in emails}

        try:
            mail.send_mail(title,
                emails["plain"],
                settings.EMAIL_FROM_ADDRESS,
                [self.email],
                html_message = emails["html"])

        except ConnectionRefusedError:
            logger.error("Failed to send email to %s, connection refused!",self.email)
            return False
        else:
            logger.info("Sent email to %s",self.email)
            self.mailed = True
            self.save()
            return True

    def __str__(self):
        return f"Invitation for {self.email}"

class CountryAssignment(BaseModel):
    name: constr(strip_whitespace=True,regex="^[a-zA-Z -]+$")
    assigned: bool

class InvitationRow(BaseModel):
    position: str
    affiliation: str
    email: EmailStr 
    countries: List[str] 

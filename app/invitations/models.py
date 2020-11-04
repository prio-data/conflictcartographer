import re
import os
from typing import List

import logging

from pydantic import BaseModel,EmailStr,constr

import markdown

from django.conf import settings

from django.template import Template,Context
from django.template.loader import render_to_string

from django.db.models import CharField,Model,OneToOneField,ManyToManyField,TextChoices
from django.db.models import BooleanField,JSONField,EmailField,CASCADE,TextField

from django.contrib.auth.models import User

from django.core import mail 
from django.db.utils import IntegrityError

from django.utils.translation import gettext_lazy

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
        
        try:
            md = markdown.Markdown()
            et = EmailTemplate.objects.filter(active=True,email_type="inv")[0]
            msg = et.render({"link":self.invitationLink()})
            call = {
                "subject": et.subject,
                "message":re.sub("\[[^\)]+",self.invitationLink(),et.message),
                "html_message":msg,
            }

        except IndexError:
            call = [
                ("message",settings.DEFAULT_PLAINTEXT_MAIL_TEMPLATE),
                ("html_message",settings.DEFAULT_HTML_MAIL_TEMPLATE)]
            call = {k:render_to_string(template,{"link":self.invitationLink()})
                for k,template in call}
            call.update({"subject":settings.DEFAULT_EMAIL_TITLE})

        call.update({
                "from_email":settings.EMAIL_FROM,
                "recipient_list":[self.email]
            })

        try:
            mail.send_mail(**call)

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

class EmailTemplate(Model):
    """
    An editable email template which is used to draft invitation emails interactively
    """
    class EmailTypes(TextChoices):
        INVITATION  = "inv", gettext_lazy("invitation")
        REMINDER = "rem", gettext_lazy("reminder")

    subject = CharField(max_length=1024,default=settings.DEFAULT_EMAIL_TITLE)
    message = TextField(default="[{{link}}](Click this link to participate)")

    active = BooleanField(default=False)
    email_type = CharField(
            max_length=3,
            choices=EmailTypes.choices,
            default=EmailTypes.INVITATION)

    def render(self,context):
        md = markdown.Markdown()
        return md.convert(Template(self.message).render(Context(context)))

    def __str__(self):
        return f"{self.email_type} - \"{self.subject}\""

class CountryAssignment(BaseModel):
    name: constr(strip_whitespace=True,regex="^[a-zA-Z -]+$")
    assigned: bool

class InvitationRow(BaseModel):
    position: str
    affiliation: str
    email: EmailStr 
    countries: List[str] 

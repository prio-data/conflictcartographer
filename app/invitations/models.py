from typing import List

import logging

from django.conf import settings

from django.db.models import CharField,Model,OneToOneField
from django.db.models import BooleanField,JSONField,EmailField,CASCADE

from django.contrib.auth.models import User

from django.core import mail 
from django.template.loader import render_to_string
from django.db.utils import IntegrityError

from api.models import Country

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

    refkey = CharField(max_length = 32, unique = True)

    mailed = BooleanField()
    metadata = JSONField()

    @classmethod
    def create(cls, email: str, countries: List[int]):
        """
        Create an invite from an email and a list of countries 
        """
        countries = Country.objects.filter(pk__in = countries)
        refkey = referralKeygen(email)
        
        invite = cls(email = email, refkey = refkey)

        try:
            invite.save()

        except IntegrityError:
            logger.warning("Invitation for %s already exists!",email)
            invite = None

        else:
            invite.countries.set(countries)
            invite.save()
            logger.debug("Successfully created invitation for %s",email)

        return invite

    def dispatch(self):
        """
        Sends the invitation by email 
        """

        link = settings.INVITATION_LINK_BASE.format(key = self.refkey)
        title = settings.EMAIL_TITLE 

        emails = [
            ("plain",settings.PLAINTEXT_MAIL_TEMPLATE),
            ("html",settings.HTML_MAIL_TEMPLATE)]

        emails = {k:render_to_string(template,{"link":link})
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
        return f"Invitation for {self.email} ({self.invitation_status()})"

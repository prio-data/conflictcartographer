
import hashlib
from bs4 import BeautifulSoup

from django.core import mail
from django.test import TestCase
from django.conf import settings

from django.contrib.auth.models import User

import re

from invitations.models import Invitation
from invitations.util import referralKeygen

class InvitationTest(TestCase):
    serialized_rollback = True

    def test_dispatch_and_register(self):
        i = Invitation(email="name@loc.com")
        i.dispatch()

        m = mail.outbox[0]

        # Mailed flag
        self.assertTrue(i.mailed)

        # Email has proper title
        self.assertEqual(m.subject, settings.EMAIL_TITLE)

        # Email contains ref. key
        self.assertIsNotNone(re.search(i.refkey,m.body))

        r = self.client.get(i.invitationLink(),follow=True)
        location,code = r.redirect_chain[-1]
        soup = BeautifulSoup(r.content,features="html.parser")

        regform = soup.find("form")
        usernameInput = regform.find("input",attrs={"name":"username"})

        # Email is in the username form
        self.assertEqual(usernameInput["value"],i.email)

        url = regform.action if regform.action else location 
        method = regform.method if regform.method else "POST"

        getattr(self.client,method.lower())(url,{
                "username": usernameInput["value"],
                "password1": hashlib.md5(b"1234").hexdigest(),
                "password2": hashlib.md5(b"1234").hexdigest()
            })

        # User was created 
        try:
            u = User.objects.get(email = i.email)
        except User.DoesNotExist:
            self.fail("User was not created")

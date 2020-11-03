import csv
import io

from typing import Dict

import hashlib
from bs4 import BeautifulSoup

from django.core import mail
from django.test import TestCase,Client
from django.conf import settings
from django import urls

from django.contrib.auth.models import User

import re

from invitations.models import Invitation
from invitations.util import referralKeygen
from invitations.services import bulkCreateInvites,parseInviteFile
from api.models import Country

EXAMPLE_CSV = [
    "name,email,position,affiliation,one,two,thr,fou,fiv,six,sev,eig",
    "name nameson,one@one.com,plumber,Somewhere,1,1,1,1,1,0,0,0",
    "name nameson,two@two.com,cleaner,Someplace,0,0,0,1,1,1,1,1",
    "name nameson,thr@thr.com,cleaner,Somewhere,1,1,1,1,1,0,0,0",
    "name nameson,fou@fou.com,plumber,Somewhere,0,0,0,1,1,1,1,1",
    "name nameson,fiv@fiv.com,cleaner,Someplace,1,1,1,1,1,0,0,0",
]


class InvitationTest(TestCase):
    serialized_rollback = True

    def test_dispatch_and_register(self):
        """
        Long-form test that tests creating and sending an invite, and then
        registering a user by following the referral link in the invitation email.
        """
        countries = [Country(gwno=i,name=str(i),shape={},simpleshape={}) for i in range(5)]
        for c in countries:
            c.save()

        i = Invitation(email="name@loc.com")
        i.save()
        i.countries.set(countries)
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


        # Make sure all countries were added
        self.assertEqual(
                {c.pk for c in countries},
                {c.pk for c in u.profile.countries.all()}
            )

    def test_parse(self):
        """
        Tests parsing an invite-csv
        """
        f = io.StringIO("\n".join(EXAMPLE_CSV))
        reader = csv.DictReader(f)
        parsed = parseInviteFile(reader)

        f.seek(0)
        reader = csv.DictReader(f)
        rows = [*reader]
        self.assertEqual(len(parsed),len(rows))

        for v in ("email","affiliation","position"):
            self.assertEqual(
                    [getattr(r,v) for r in parsed],
                    [r[v] for r in rows]
                )

    def test_bulk_invite(self):
        """
        Tests importing and dispatching invites from a csv
        """
        N = ("one","two","thr","fou","fiv","six","sev","eig")
        countries = [Country(gwno=i+1,name=n,shape={},simpleshape={}) for i,n in zip(range(8),N)]
        for c in countries:
            c.save()

        f = io.StringIO("\n".join(EXAMPLE_CSV))
        reader = csv.DictReader(f)
        parsed = parseInviteFile(reader)

        invites = bulkCreateInvites(parsed)

        furtherInvites = bulkCreateInvites(parsed)
        self.assertEqual(len(furtherInvites),0)

        for i in invites:
            i.dispatch()

        for parsedrow,invite,email in zip(parsed,invites,mail.outbox):
            self.assertEqual(email.to[-1],invite.email)
            self.assertEqual(invite.email,parsedrow.email)
            self.assertEqual(
                    set(parsedrow.countries),
                    {c.name for c in invite.countries.all()}
                )
            self.assertIsNotNone(re.search(invite.refkey,email.body))

    def test_admin_dispatch(self):
        """
        Tests admin action to send email to selected invites
        """
        user = User.objects.create_superuser(username="admin",email="admin@admin.com",password="admin")
        self.client.login(username="admin",password="admin")

        invites = [Invitation(email=f"{i}@{i}.com") for i in range(5)]
        for i in invites:
            i.save()

        url = urls.reverse("admin:invitations_invitation_changelist")
        data = {'action': 'dispatch_invitation',
                '_selected_action': [i.pk for i in invites]}

        r = self.client.post(url,data,follow=True)
        self.assertEqual(r.status_code,200)
        self.assertEqual(len(invites),len(mail.outbox))

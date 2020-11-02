import os
import logging

from typing import List,Iterable,Dict

from django.conf import settings
from django.core import exceptions, validators
from django.db import IntegrityError

import json

from hashlib import md5

from api.models import Country
from invitations.models import CountryAssignment,InvitationRow,Invitation

logger = logging.getLogger(__name__)

# ==============================================
# Data import

def parseInviteFile(lod: Iterable[Dict[str,str]])->List[InvitationRow]:
    NONCOUNTRIES = ["email","position","affiliation","name"]

    first = next(lod)
    countries = [h for h in first.keys() if h not in NONCOUNTRIES]

    def parseRow(row):
        ncrow = {k:v for k,v in row.items() if k in NONCOUNTRIES}
        ctries = [CountryAssignment(name=k,assigned=v) for k,v in row.items() if k not in NONCOUNTRIES]
        return InvitationRow(**ncrow,countries = [c.name for c in ctries if c.assigned])

    inviteRows = [parseRow(first)]+[parseRow(r) for r in lod]
    return inviteRows 

def bulkCreateInvites(data: List[InvitationRow], cohort = None)->List[Invitation]:
    invitations = []
    for entry in data:
        try:
            Invitation.objects.get(email=entry.email)
        except Invitation.DoesNotExist:
            invitation = Invitation(
                    email = entry.email,
                    metadata = {"position": entry.position,"affiliation": entry.affiliation}
                )
            invitation.save()
            
            countries = []
            for cname in entry.countries:
                try:
                    c = Country.objects.get(name=cname)
                except Country.DoesNotExist:
                    logger.warning(f"Did not find country {cname} while creating invite for {entry.email}")
                else:
                    countries.append(c)

            invitation.countries.set(countries)

            invitations.append(invitation)
        else:
            logger.warning(f"Invitation for {entry.email} already exists!")

    return invitations 

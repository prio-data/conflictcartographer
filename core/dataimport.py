
from django.conf import settings
from django.core import exceptions, validators


from core.models import Invitation, Cohort

import json

from hashlib import md5

# ==============================================
# Data import

def bulkCreateInvite(data, cohort = None):
    """
    Utility function

    Takes a list of dicts with the following data:
    email: User email
    projects: A list of project numbers (pk's)

    Also takes an optional cohort argument (a cohort object).
    If none is supplied, a new cohort is created. 
    """

    def formatIsValid(d):
        try: 
            d["email"]
            d["projects"]
        except KeyError: 
            print("An entry did not have enough keys")
            res = False
        else:
            res = True
        return res

    def emailIsValid(d):
        e = d["email"]
        try: 
            validators.validate_email(e)
        except exceptions.ValidationError:
            print(f"{e} is not a valid email address")
            res = False
        else:
            res = True
        return res

    for check in [formatIsValid, emailIsValid]:
        data = [d for d in data if check(d)]

    if cohort is None:
        stamp = md5(json.dumps(data).encode()).hexdigest()[0:10]

        isnew = ""
        try :
            cohort = Cohort.objects.get(stamp = stamp)
        except Cohort.DoesNotExist:
            cohort = Cohort(stamp = stamp)
            cohort.save()
            isnew = "new "

    invitations = [Invitation.create(d["email"],d["projects"],cohort) for d in data]

    for i in [i for i in invitations if i is not None]:
        try:
            i.save()
        except IntegrityError:
            print(f"Invitation for {i.email} already exists!")

    return cohort

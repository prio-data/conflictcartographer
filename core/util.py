
import psycopg2

from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User

from django.conf import settings
from django.core import mail, exceptions, validators

from django.template.loader import render_to_string

from hashlib import md5

from api.models import Project
from core.models import Invitation, Cohort

import json
import time


# ================================================
# INVITE STUFF

def generateRefKey(email):
    """
    Creates a unique indentifier key that is used to recieve
    users that have been invited.
    """

    salted = email+settings.SECRET_KEY
    hashed = md5(email.encode()).hexdigest()
    return hashed 

def createInvite(email, projects, cohort = False):
    """
    Creates and pushes an invite object to the database from 
    raw data.
    """

    key = generateRefKey(email)
    projects = Project.objects.filter(pk__in = projects)

    try:
        Invitation.objects.get(refkey = key)
    except Invitation.DoesNotExist:
        i = Invitation(email = email, refkey = key)

        if cohort:
            i.cohort = cohort

        i.save()
        i.projects.set(projects)
        i.save()

    else:
        print(f"Invitation for {email} ({key}) already exists!")
        i = None

    return i

def bulkCreateInvite(data, cohort = None):
    """
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

    invitations = [createInvite(d["email"],d["projects"],cohort) for d in data]
    invitations = [i for i in invitations if i is not None]

    print(f"created {len(invitations)} in {isnew}cohort {cohort.name} ({cohort.stamp})")

    return cohort

def dispatchInvite(invitation):
    """
    Sends an invitation to an invitationd user by email, containing the unique
    link used to log on.

    This function should CASE, based on what the invitation status is.
    """
    print(invitation.invitation_status())

    key = invitation.refkey
    link = settings.INVITATION_LINK_BASE.format(key = key) 
    try:
        interval = settings.EMAIL_INTERVAL
    except AttributeError:
        interval = 1

    msg_plain = render_to_string("mail/invitation.txt",{"uniquelink":link})
    msg_html = render_to_string("mail/invitation.html",{"uniquelink":link})

    try:
        res = mail.send_mail("Invitation to participate in a geo-spatial expert survey",
            msg_plain,
            settings.EMAIL_FROM_ADDRESS,
            [invitation.email], html_message = msg_html)

    except ConnectionRefusedError:
        return False

    else:
        invitation.reached = True 
        invitation.save()
        time.sleep(interval)
        return True

def dispatchCohort(cohort):
    """
    Emails all of the invitations in a Cohort (object).
    """

    invitations = cohort.invitations.all()

    results = [dispatchInvite(i) for i in invitations]
    results = zip(invitations,results)
    
    succeeded = [i for i,res in results if res] 
    failed = [i for i,res in results if not res] 

    for i in succeeded:
        print(f"Sent email to {i.email}")

    for i in failed:
        print(f"Failed to email {i.email}")

#def bulkCreateUsers(data):
    #
    #for d in data:
#
        #d["username"] = d["email"]
#
        #pw = makePassword(d)
        #for k in ["password1","password2"]:
            #d[k] = pw
#
    #usernames = [d["username"] for d in data]
#
    #exists = []
    #new = []
    #for name in usernames:
        #if userExists(name):
            #exists.append(name)
        #else:
            #new.append(name)
    #
    ## Create new users
    #newUserData = [d for d in data if d["username"] in new] 
    #forms = [UserCreationForm(d) for d in newUserData]
    #forms = [f for f in forms if f.is_valid()]
#
    #newusers = [f.save() for f in forms]
#
    ## Get existing users
    #existingusers = [User.objects.get(username = name) for name in exists]
    #users = newusers + existingusers
    #
    ## Update all users
    #for user in users:
        #userdata = [d for d in data if d["username"] == user.username][0]
        #user.email = userdata["email"]
        #print(f"""
            #{user.username}
            #{user.email}
        #""")
        ## projects
        #projects = Project.objects.filter(pk__in = userdata["projects"])
        #user.projects.set(projects)
#
        #user.save()
        ##user.delete()
#
    #return f"created {len(newusers)} users | updated {len(existingusers)} users"

# ================================================
# Utility functions

def userExists(uname):
    try:
        User.objects.get(username = uname)
    except User.DoesNotExist:
        return False
    else:
        return True


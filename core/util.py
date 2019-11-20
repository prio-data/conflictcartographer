
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User

from django.conf import settings
from django.core import mail

from hashlib import md5

from api.models import Project
from core.models import Invitation


SALT = "beagoodboy"

def userExists(uname):
    try:
        User.objects.get(username = uname)
    except User.DoesNotExist:
        return False
    else:
        return True

def generateRefKey(email):
    salted = "pleasewelcome"+email+settings.SECRET_KEY
    hashed = md5(email.encode()).hexdigest()
    print(hashed)
    return hashed 

def createInvite(email, projects, cohort = False):
    key = generateRefKey(email)
    projects = Project.objects.filter(pk__in = projects)

    i = Invitation(email = email, refkey = key)

    if cohort:
        i.cohort = cohort

    i.save()
    i.projects.set(projects)
    i.save()

    return i

def dispatchInvite(invite):

    try:
        res = mail.send_mail("Your invitation",
            f"Please go to localhost:8000/accounts/ref/{invite.refkey}/",
            settings.EMAIL_HOST_USER,
            [invite.email])

    except ConnectionRefusedError:
        invite.reached = False 
        invite.save()
        return False

    else:
        invite.reached = True
        invite.save()
        return True

 
def bulkCreateUsers(data):
    
    for d in data:

        d["username"] = d["email"]

        pw = makePassword(d)
        for k in ["password1","password2"]:
            d[k] = pw

    usernames = [d["username"] for d in data]

    exists = []
    new = []
    for name in usernames:
        if userExists(name):
            exists.append(name)
        else:
            new.append(name)
    
    # Create new users
    newUserData = [d for d in data if d["username"] in new] 
    forms = [UserCreationForm(d) for d in newUserData]
    forms = [f for f in forms if f.is_valid()]

    newusers = [f.save() for f in forms]

    # Get existing users
    existingusers = [User.objects.get(username = name) for name in exists]
    users = newusers + existingusers
    
    # Update all users
    for user in users:
        userdata = [d for d in data if d["username"] == user.username][0]
        user.email = userdata["email"]
        print(f"""
            {user.username}
            {user.email}
        """)
        # projects
        projects = Project.objects.filter(pk__in = userdata["projects"])
        user.projects.set(projects)

        user.save()
        #user.delete()

    return f"created {len(newusers)} users | updated {len(existingusers)} users"


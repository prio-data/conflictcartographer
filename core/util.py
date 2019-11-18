
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User

from hashlib import md5

from api.models import Project

SALT = "beagoodboy"

def userExists(uname):
    try:
        User.objects.get(username = uname)
    except User.DoesNotExist:
        return False
    else:
        return True

def makePassword(entry):

    pw = entry["username"]+SALT
    pw = md5(pw.encode()).hexdigest()
    print(pw)

    return pw
 
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


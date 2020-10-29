import csv
from adminext.models import InvitationRow,CountryAssignment
from core.models import Invitation
import logging
from pydantic import ValidationError

logger = logging.getLogger(__name__)

def updateInvitations(data):
    """
    Update invitations a "list of dictionary"-type iterator from a CSV file.
    """
    NONCOUNTRIES = ("name","affiliation","type","email","comment","Expert")
    resp = ""

    for row in data:
        try:
            countries = []
            for k,v in {k:v for k,v in row.items() if k not in NONCOUNTRIES}.items():
                try:
                    countries.append(CountryAssignment(name=k,assigned=v))
                except ValidationError:
                    pass

            valInv = InvitationRow(
                    name = row["name"],
                    position = row["type"],
                    affiliation = row["affiliation"],
                    email = row["email"],
                    countries = [c.name for c in countries if c.assigned]
                    )

            try:
                inv = Invitation.create(
                        email=valInv.email,
                        projects=[]
                    )
                inv.save()
            except AttributeError:
                pass
        except ValidationError:
            resp += "error"
            continue 

        resp += str(valInv)
        resp += "\n\n"
    return resp 


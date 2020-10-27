
from django.contrib.auth import login,authenticate
import base64

HEADER_ENCODING = "iso-8859-1"

def authenticateRequest(request):
    """
    Not sure why i needed this, authenticates with a HTTP header containing uname/pw
    """
    decode = lambda x, encoding: base64.b64decode(x).decode(encoding)

    def getAuth(header):
        decoded = decode(header.split()[1], HEADER_ENCODING) 
        return(decoded.split(":"))
    
    try:
        username, password = getAuth(request.headers["Authorization"]) 
        user = authenticate(username = username, password = password)
        login(request,user)

    except (AttributeError, KeyError):
        return False

    else:
        return True


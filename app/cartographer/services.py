import math
import datetime

def getQuarter(date: datetime.date)->int:
    return math.ceil((date.month / 12) * 4)

def currentQuarter()->int:
    return getQuarter(datetime.date.today())

def currentYear()->int:
    return datetime.date.today().year

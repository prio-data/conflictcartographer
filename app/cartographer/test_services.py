
import datetime
from django.test import TestCase
from cartographer.services import getQuarter,currentQuarter

class ServiceTests(TestCase):

    def test_time_serv(self):
        self.assertEqual(getQuarter(datetime.date(1999,1,1)),1)
        self.assertEqual(getQuarter(datetime.date(1999,4,1)),2)
        self.assertEqual(getQuarter(datetime.date(1999,7,1)),3)
        self.assertEqual(getQuarter(datetime.date(1999,10,1)),4)

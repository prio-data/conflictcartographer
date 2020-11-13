import datetime
from django.test import TestCase
from cartographer.services import getQuarter,currentQuarter,quarters,quarterRange

class ServiceTests(TestCase):

    def test_time_serv(self):
        self.assertEqual(getQuarter(datetime.date(1999,1,1)),1)
        self.assertEqual(getQuarter(datetime.date(1999,4,1)),2)
        self.assertEqual(getQuarter(datetime.date(1999,7,1)),3)
        self.assertEqual(getQuarter(datetime.date(1999,10,1)),4)

    def test_qrange(self):
        qr = quarterRange(datetime.date(year=1999,month=2,day=10))
        self.assertEqual(quarterRange(datetime.date(year=1999,month=2,day=10)),(
                datetime.date(year=1999,month=1,day=1),
                datetime.date(year=1999,month=3,day=1)
            ))

        self.assertEqual(quarterRange(datetime.date(year=2001,month=4,day=10)),(
                datetime.date(year=2001,month=4,day=1),
                datetime.date(year=2001,month=6,day=1)
            ))

        self.assertEqual(quarterRange(datetime.date(year=2001,month=8,day=10)),(
                datetime.date(year=2001,month=7,day=1),
                datetime.date(year=2001,month=9,day=1)
            ))

        self.assertEqual(quarterRange(datetime.date(year=2001,month=12,day=10)),(
                datetime.date(year=2001,month=10,day=1),
                datetime.date(year=2001,month=12,day=1)
            ))

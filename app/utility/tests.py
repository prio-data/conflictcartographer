import unittest
from utility.geojsontypes import *

class TestGeoJSONValidation(unittest.TestCase):
    def test_test(self):
        try:
            point = Point(**{"type":"Point","coordinates":[.5,.5]})
            
            pol = Polygon(**{
                "type":"Polygon",
                "coordinates": [
                    [.1,.1],[.2,.2],[.3,.3],[.1,.1]
                ]
            })

            mpol = MultiPolygon(**{
                "type":"MultiPolygon",
                "coordinates":[
                    [[.5,.5],[.1,.1],[.2,.2],[.5,.5]],
                    [[.1,.1],[.5,.5],[.3,.3],[.1,.1]],
                ]
            })

            ftrs = []
            for g in [point,pol,mpol]:
                ft = Feature(**{
                    "type":"Feature",
                    "geometry":g,
                    "properties":{
                        "foo":1,
                        "bar":"baz",
                    }
                })
                ftrs.append(ft)

            FeatureCollection(**{
                "type":"FeatureCollection",
                "features":ftrs
            })
        except Exception as e:
            self.fail()


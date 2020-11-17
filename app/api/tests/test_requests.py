"""
Testing API requests
"""
import json

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from api.models import Country

class ApiRequestsTest(TestCase):
    def setUp(self):
        self.u = User.objects.create_user(username="testuser",password="12345")
        c = Country.objects.create(name="somewhere",iso2c="SW",gwno=1,shape={},simpleshape={})
        self.u.profile.countries.set([c])

    def test_crud(self):
        # Test disallowed without login
        for method,url in [("get","assigned"),("post","shape-list")]:
            self.assertEqual(getattr(self.client,method)(reverse(url)).status_code,403)

        login = self.client.login(username="testuser",password="12345")
        self.assertTrue(login)

        # Get assigned countries
        countries = self.client.get(reverse("assigned"))
        self.assertEqual(countries.status_code,200)

        countries = json.loads(countries.content.decode())
        self.assertEqual(countries[0]["gwno"],1)

        # Test posting a shape
        requestData = {
            "shape":{},
            "intensity":5,
            "confidence":5,
            "country":countries[0]["url"]
            }

        r = self.client.post(reverse("shape-list"),requestData,content_type="application/json")
        self.assertEqual(r.status_code,201)

        # Test posting a shape with arbitrary data
        requestData = {
            "shape":{},
            "values":{"something":"else","entirely":[1,2,3,4,5]},
            "country":countries[0]["url"]
            }

        r = self.client.post(reverse("shape-list"),requestData,content_type="application/json")
        self.assertEqual(r.status_code,201)

        # Assert that data is properly stored 
        r = self.client.get(reverse("shape-list"),content_type="application/json")
        self.assertEqual(r.status_code,200)
        shapes = json.loads(r.content.decode())
        s1,s2 = shapes
        self.assertEqual(s1["values"],{"intensity":5,"confidence":5})
        self.assertEqual(s2["values"],{"something":"else","entirely":[1,2,3,4,5]})

        # Assert that project status is correct 
        r = self.client.get(reverse("projectstatus",kwargs={"project":1}))
        self.assertEqual(r.status_code,200)
        data = json.loads(r.content.decode())
        self.assertEqual(data["shapes"],2)

        # Delete a shape 

        d = json.loads(self.client.get(reverse("shape-list"),content_type="application/json").content.decode())
        s1,s2 = d

        r = self.client.delete(s1["url"],content_type="application/json")
        self.assertEqual(r.status_code,204)

        r = self.client.get(reverse("projectstatus",kwargs={"project":1}))
        self.assertEqual(r.status_code,200)
        data = json.loads(r.content.decode())
        self.assertEqual(data["shapes"],1)

        # Update a shape 
        s2["values"] = {"a third option":3}
        r = self.client.put(s2["url"],s2,content_type="application/json")
        self.assertEqual(r.status_code,200)

        r = self.client.get(s2["url"],content_type="application/json")
        self.assertEqual(r.status_code,200)
        self.assertEqual(json.loads(r.content.decode()),s2)

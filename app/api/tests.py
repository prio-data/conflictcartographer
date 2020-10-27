
from django.test import TestCase
from rest_framework import test, status
import requests

class AdminTesting(TestCase):
    def setUp(self):
        self.client = test.RequestsClient()

        r = self.client.get("http://testserver/")

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.csrftoken = r.cookies["csrftoken"]

    def test_can_reach_api(self):
        response = self.client.get("http://localhost:8000/api/",
            headers = {"X-CSRFToken": self.csrftoken})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


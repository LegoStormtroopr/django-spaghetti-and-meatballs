from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import setup_test_environment

setup_test_environment()


class LoadThePlate(TestCase):
    def test_plate(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Officer' in response.content)

    def test_plate_with_settings(self):
        response = self.client.get("/test/plate_settings")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Officer' not in response.content)

    def test_plate_with_override_settings(self):
        response = self.client.get("/test/plate_override")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('policeofficer' in response.content.lower())
        self.assertTrue('policestation' not in response.content.lower())

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import setup_test_environment

setup_test_environment()

class LoadThePlate(TestCase):
    def test_plate(self):
        home = self.client.get("/")
        self.assertEqual(home.status_code,200)

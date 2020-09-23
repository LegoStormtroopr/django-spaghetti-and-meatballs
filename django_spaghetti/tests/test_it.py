from django.test import TestCase
from django.urls import reverse


class LoadThePlate(TestCase):
    def test_plate(self):
        response = self.client.get("/plate")
        resp_str = str(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Officer' in resp_str)
        self.assertTrue('All arrests made by the officer' not in resp_str)

    def test_plate_with_settings(self):
        response = self.client.get("/test/plate_settings")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Officer' not in str(response.content))

    def test_plate_show_m2m_field_detail(self):
        response = self.client.get("/test/plate_show_m2m_field_detail")
        resp_str = str(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Officer' in resp_str)
        self.assertTrue('All arrests made by the officer' in resp_str)

    def test_plate_with_override_settings(self):
        response = self.client.get("/test/plate_override")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('policeofficer' in str(response.content).lower())
        self.assertTrue('policestation' not in str(response.content).lower())

    def test_no_override_after_override(self):
        response1 = self.client.get("/test/plate_override")
        response2 = self.client.get("/plate")
        resp_str = str(response2.content)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertTrue('policeofficer' in str(response1.content).lower())
        self.assertTrue('policestation' not in str(response1.content).lower())
        self.assertTrue('Officer' in resp_str)
        self.assertTrue('All arrests made by the officer' not in resp_str)

    def test_meatball(self):
        response = self.client.get("/test/plate_show_m2m_field_detail")
        resp_str = str(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('IntegerField' in resp_str)
        self.assertTrue('CharField' in resp_str)
        self.assertTrue('ManyToManyField' in resp_str)
        self.assertTrue('ForeignKey' in resp_str)
        self.assertTrue('OneToOneField' in resp_str)
        self.assertTrue('DateField' in resp_str)
        self.assertTrue('URLField' not in resp_str)

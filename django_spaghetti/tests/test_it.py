from django.test import TestCase


class LoadThePlate(TestCase):
    def test_plate(self):
        response = self.client.get("/plate")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Officer')
        self.assertContains(response, 'All arrests made by the officer')

    def test_plate_with_settings(self):
        response = self.client.get("/test/plate_settings")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Officer')

    def test_plate_show_m2m_field_detail(self):
        response = self.client.get("/test/plate_show_m2m_field_detail")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Officer')
        self.assertContains(response, 'All arrests made by the officer')

    def test_plate_with_override_settings(self):
        response = self.client.get("/test/plate_override")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('policeofficer' in str(response.content).lower())
        self.assertTrue('policestation' not in str(response.content).lower())

    def test_no_override_after_override(self):
        response1 = self.client.get("/test/plate_override")
        response2 = self.client.get("/plate")
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertTrue('policeofficer' in str(response1.content).lower())
        self.assertTrue('policestation' not in str(response1.content).lower())
        self.assertContains(response1, 'Officer')
        self.assertNotContains(response1, 'All arrests made by the officer')

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

from django.test import TestCase

# Create your tests here.

class SmokeTest(TestCase):

    def test_fail_direct(self):
        self.assertEqual(1,2)

from django.apps import apps
from django.test import TestCase
from .apps import DonationsConfig

class TestDonationsConfig(TestCase):
    def test_app(self):
        self.assertEqual("donations", DonationsConfig.name)

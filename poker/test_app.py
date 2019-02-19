from django.apps import apps
from django.test import TestCase
from .apps import PokerConfig

class TestPokerConfig(TestCase):
    def test_app(self):
        self.assertEqual("poker", PokerConfig.name)
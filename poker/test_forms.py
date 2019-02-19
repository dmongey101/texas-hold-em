from django.test import TestCase
from .forms import CreateTableForm

# Create your tests here.

class TestCreateTableForm(TestCase):
    
    def test_CreateTableForm_is_valid(self):
        form = CreateTableForm({'name' : 'Test Table', 'no_of_players': 3, 'blinds': 10})
        self.assertTrue(form.is_valid())
from django.test import TestCase
from django.contrib.auth.models import User
from .forms import MakePaymentForm, OrderForm

# Create your tests here.
class TestDonationsViews(TestCase):
    
    def test_get_donations_page(self):
        User.objects.create_user(username='test', email='test@example.com', password='Madetotest')
        self.client.login(username='test', password='Madetotest')
        page = self.client.get("/donations/pay", follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "donations/donations.html")
from django.test import TestCase
from django.contrib.auth.models import User
from .forms import SignUpForm

# Create your tests here.
class TestAccountsViews(TestCase):
    
    def test_get_signup_page(self):
        page = self.client.get("/accounts/signup/", follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "registration/signup.html")
        
   
    def test_user_can_signup(self):
        response = self.client.post("/accounts/signup/", {
            'username': 'test',
            'email': 'test@email.com',
            'password1': 'Testpassword',
            'password2': 'Testpassword'
        })
        self.assertRedirects(response, '/', status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        
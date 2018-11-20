from django import forms
from .models import Table

class CreateTableForm(forms.ModelForm):
    class Meta:
        model = Table
        exclude = ('chips', 'big_blind')
        

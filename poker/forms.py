from django import forms
from .models import Table, Player, Hand

class CreateTableForm(forms.ModelForm):
    class Meta:
        model = Table
        widgets = {
        'password': forms.PasswordInput(),
        }
        exclude = ('is_active', 'big_blind', 'small_blind', 'dealer', )


        

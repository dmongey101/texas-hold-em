from django import forms
from .models import Table, Player, Hand

class CreateTableForm(forms.ModelForm):
    class Meta:
        model = Table
        exclude = ('is_active', 'big_blind', 'small_blind', 'dealer', 'owner', )


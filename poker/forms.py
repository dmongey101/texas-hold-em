from django import forms
from .models import Table, Player, Hand

class CreateTableForm(forms.ModelForm):
    class Meta:
        model = Table
        exclude = ('current_player', )


        

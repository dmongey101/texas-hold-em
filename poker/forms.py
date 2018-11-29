from django import forms
from .models import Table, Player, Hand

class CreateTableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = "__all__"
        
        
class CreatePlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = "__all__"
        
        
class CreateHandForm(forms.ModelForm):
    class Meta:
        model = Hand
        fields = "__all__"
        

        

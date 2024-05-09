from django import forms
from .models import Ocena, OcenaSerial


class OcenaFilmuForm(forms.ModelForm):
    class Meta:
        model = Ocena
        fields = ['ocena']

class OcenaSerialuForm(forms.ModelForm):
    class Meta:
        model = OcenaSerial
        fields = ['ocena']

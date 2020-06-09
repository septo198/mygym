from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CorsoForm(forms.Form):
    nome = forms.CharField(max_length=100, label='Nome', required=False, initial="")
    """prezzo_max = forms.FloatField(label='Prezzo massimo', required=False, initial=0)"""


from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit

User = get_user_model()

class CorsoForm(forms.Form):
    nome = forms.CharField(max_length=100, label='Nome corso', required=False, initial="")
    prezzo_max = forms.FloatField(label='Prezzo massimo', required=False, initial=0)

class ClienteSignUpForm(UserCreationForm):
    foto_profilo = forms.ImageField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_cliente = True
        user.foto_profilo = self.cleaned_data.get('foto_profilo')
        user.save()
        Cliente.objects.create(user=user)
        return user

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("La mail selezionata è già esistente")
        return data

class PtSignUpForm(UserCreationForm):
    foto_profilo = forms.ImageField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_pt = True
        user.foto_profilo = self.cleaned_data.get('foto_profilo')
        user.save()
        Pt.objects.create(user=user)
        return user

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("La mail selezionata è già esistente")
        return data

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class IscrizioneAddForm(forms.ModelForm):
    class Meta:
        model = Iscrizione
        fields = ('mesi_durata',)

class CorsoAddForm(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = Corso
        exclude = ('iscritti_attuali', 'posti_rimanenti',)

    def save(self, commit=True):
        corso = super().save(commit=False)
        corso.foto = self.cleaned_data.get('foto')
        corso.save()
        return corso

class UserUpdateForm(forms.Form):
    image = forms.ImageField(label='Aggiorna immagine profilo')

class UserSearchForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )




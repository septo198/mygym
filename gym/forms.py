from django import forms
from django.forms import DateInput

from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth import get_user_model

#Definisco quale classe user utilizzare
User = get_user_model()

#Form ricerca di un corso
class CorsoForm(forms.Form):
    nome = forms.CharField(max_length=100, label='Nome corso', required=False, initial="")
    prezzo_max = forms.FloatField(label='Prezzo massimo', required=False, initial=10000)

#Form registrazione di un cliente
class ClienteSignUpForm(UserCreationForm):
    foto_profilo = forms.ImageField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_cliente = True
        user.foto_profilo = self.cleaned_data.get('foto_profilo') #Aggiungo la foto profilo
        user.save()
        Cliente.objects.create(user=user)
        return user

    #Gestisco l'unicità della email
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("La mail selezionata è già esistente")
        return data

#Form registrazione personal trainer
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

    #Gestisco unicità mail
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("La mail selezionata è già esistente")
        return data

#Form creazione utente generico
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    #Controllo che le password combacino
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

#Form aggiunta iscrizione
class IscrizioneAddForm(forms.ModelForm):
    class Meta:
        model = Iscrizione
        fields = ('mesi_durata',)

#Form aggiunta corso
class CorsoAddForm(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = Corso
        exclude = ('iscritti_attuali', 'posti_rimanenti',)

    def save(self, commit=True):
        corso = super().save(commit=False)
        corso.foto = self.cleaned_data.get('foto')  #Foto corso
        corso.save()
        return corso

#Form per aggiornare immagine profilo sul proprio profilo utente
class UserUpdateForm(forms.Form):
    image = forms.ImageField(label='Aggiorna immagine profilo')

#Form per la ricerca di un utente generico
class UserSearchForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )

#Form aggiunta di una nuova scheda
class SchedaAddForm(forms.ModelForm):
    class Meta:
        model = Scheda
        fields = ('nome', )

#Form ricerca di una scheda
class SchedeSearchForm(forms.Form):
    nome = forms.CharField(max_length=100, label='Nome scheda', required=False, initial="")
    autore = forms.CharField(max_length=100, label='Nome autore', required=False, initial="")

#Form aggiunta di un esercizio ad una scheda
class EsercizioAddForm(forms.ModelForm):
    class Meta:
        model = Esercizio
        fields = ('nome_esercizio', 'ripetizioni', 'serie', 'recupero', )

#Form di aggiunta di una prenotazione sul calendario di un pt
class PrenotazioneAddForm(forms.ModelForm):
    class Meta:
        model = Prenotazione
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'date': DateInput(),
            'start_time': DateInput(attrs={'type': 'time-local'}, format='%H:%M'),
            'end_time': DateInput(attrs={'type': 'time-local'}, format='%H:%M'),
        }
        labels = {
            "date": "Data (GG/MM/AAAA)",
            "start_time": "Ora di inizio (HH:MM)",
            "end_time": "Ora di fine (HH:MM)"
        }
        fields = ('date', 'start_time', 'end_time')


from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class User(AbstractUser):
    is_cliente = models.BooleanField(default=False)
    is_pt = models.BooleanField(default=False)
    is_portinaio = models.BooleanField(default=False)
    foto_profilo = models.ImageField(upload_to='propic/', blank=True, null=True)

    @property
    def foto_profiloURL(self):
        try:
            url = self.foto_profilo.url
        except:
            url = 'images/placeholder.png'
        return url

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Pt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    #dati_reperibilità

class Portinaio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Corso(models.Model):
    nome = models.CharField(max_length=100)
    prezzo = models.FloatField(default=0)
    iscritti_max = models.IntegerField(default=0)
    iscritti_attuali = models.IntegerField(default=0)
    posti_rimanenti = models.IntegerField(blank=True, null=True, default=None)
    sedute_settimanali = models.IntegerField(default=0)
    descrizione = models.CharField(max_length=1000)
    foto = models.ImageField(upload_to='', default='placeholder.png')

    def __str__(self):
        return '{nome}, {prezzo}, {iscritti_max}, {iscritti_attuali}, {sedute_settimanali}, {descrizione}'\
            .format(nome=self.nome, prezzo=self.prezzo, iscritti_max=self.iscritti_max, iscritti_attuali=self.iscritti_attuali, sedute_settimanali=self.sedute_settimanali, descrizione=self.descrizione)

    @property
    def fotoURL(self):
        try:
            url = self.foto.url
        except:
            url = 'images/placeholder.png'
        return url

    def save(self, *args, **kwargs):
        if self.posti_rimanenti is None:
            self.posti_rimanenti = self.iscritti_max
        else:
            self.posti_rimanenti = self.iscritti_max - self.iscritti_attuali
        super(Corso, self).save(*args, **kwargs)


class Iscrizione(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    corso = models.ForeignKey(Corso, on_delete=models.SET_NULL, null=True, blank=True)
    mesi_durata = models.IntegerField(default=1)
    costo_complessivo = models.FloatField(default=0)
    pagato = models.BooleanField(default=False)
    data_iscrizione = models.DateField(default=datetime.now)
    data_scadenza = models.DateField(default='1970-01-01')

    class Meta:
        unique_together = ('corso', 'cliente',)


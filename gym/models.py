from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models import Q

class Cliente(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)

    def __str__(self):
        return '{nome}, {cognome}, {mail}'.format(nome=self.nome, cognome=self.cognome, mail=self.mail)

class Corso(models.Model):
    nome = models.CharField(max_length=100)
    prezzo = models.FloatField(default=0)
    iscritti_max = models.IntegerField(default=0)
    iscritti_attuali = models.IntegerField(default=0)
    sedute_settimanali = models.IntegerField(default=0)
    descrizione = models.CharField(max_length=1000)
    foto = models.ImageField(blank=True, null=True)

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

class Iscrizione(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    corso = models.ForeignKey(Corso, on_delete=models.SET_NULL, null=True, blank=True)
    pagato = models.BooleanField(default=False)

    class Meta:
        unique_together = ('corso', 'cliente',)

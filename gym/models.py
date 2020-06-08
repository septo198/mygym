from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models import Q

class Utente(AbstractUser):
    is_cliente = models.BooleanField(default=False)
    is_pt = models.BooleanField(default=False)
    is_portinaio = models.BooleanField(default=False)


class Cliente(models.Model):
    utente = models.OneToOneField(Utente, on_delete=models.CASCADE, primary_key=True)

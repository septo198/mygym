from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from .models import *
from django.urls import reverse

User = get_user_model()

class TestViews(TestCase):

    def setUp(self):
        self.cliente_test = User.objects.create_user(
            username="Cliente",
            password="Registration1",
            is_cliente=True
        )

        self.pt_test = User.objects.create_user(
            username="Pt",
            password="Registration1",
            is_pt=True
        )

        self.portinaio_test = User.objects.create_user(
            username="Portinaio",
            password="Registration1",
            is_portinaio=True
        )

    def clienteLogin(self):
        self.client.login(username="Cliente", password="Registration1")

    def ptLogin(self):
        self.client.login(username="Pt", password="Registration1")

    def porintaioLogin(self):
        self.client.login(username="Portinaio", password="Registration1")

    def test_profilo_no_logged_user(self):
        response = self.client.get(reverse('gym:ricerca-pt'))
        self.assertEquals(response.status_code, 302, "Utente non loggato va reindirizzato")
        self.assertRedirects(response, '/accounts/login/?next=/ricerca_pt/', status_code=302, target_status_code=200)

    def test_profilo_logged_cliente(self):
        self.clienteLogin()
        response = self.client.get(reverse('gym:ricerca-pt'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gym/ricerca_pt.html')

    def test_profilo_logged_pt(self):
        self.ptLogin()
        response = self.client.get(reverse('gym:ricerca-pt'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gym/ricerca_pt.html')

    def test_profilo_logged_portinaio(self):
        self.porintaioLogin()
        response = self.client.get(reverse('gym:ricerca-pt'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gym/ricerca_pt.html')

class TestPostiRimanenti(TestCase):

    def test_posti_rimanenti(self):
        corso = Corso()
        corso.nome = "Corso"
        corso.prezzo = 5
        corso.iscritti_max = 10
        corso.sedute_settimanali = 3
        corso.descrizione = "Sono un corso"
        corso.foto = "zumba.jpg"
        corso.save()
        self.assertEquals(10, corso.posti_rimanenti)

        corso.iscritti_attuali = 3
        corso.save()

        self.assertEquals(7, corso.posti_rimanenti)


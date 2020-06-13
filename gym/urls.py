from django.contrib.auth.decorators import login_required
from django.urls import path, include

import gym
from . import views

app_name = "gym"

urlpatterns = [
    path('', views.home, name='home'),
    path('corso_search', views.corso_search, name='corso-search'),
    path('corso_dettagli/<int:id>', views.corso_dettagli, name='corso-dettagli'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/cliente', views.ClienteSignUpView.as_view(), name='cliente-signup'),
    path('pt_page/', views.pt_page, name='pt-page'),
    path('accounts/signup/pt', views.PtSignUpView.as_view(), name='pt-signup'),
    path('logout/', views.logout, name='logout'),
    path('dettagli_utente/<int:id>/', views.utente_details, name='utente-details'),
    path('ricerca_pt/', views.ricerca_pt, name='ricerca-pt'),
    path('ricerca_cliente/', views.ricerca_cliente, name='ricerca-cliente'),
    path('aggiungi_corso/', views.aggiungi_corso, name='aggiungi-corso'),
    path('iscrizione_corso/<int:id>', views.iscrizione_corso, name='iscrizione-corso'),
    path('iscrizione_delete/<int:id>', views.iscrizione_delete, name='iscrizione-delete'),
    path('elimina_corso/<int:id>', views.elimina_corso, name='elimina-corso'),
    path('avvenuta_eliminazione_corso/', views.avvenuta_eliminazione_corso, name='avvenuta-eliminazione-corso'),
    path('salda_iscrizione/<int:id>', views.salda_iscrizione, name='salda-iscrizione'),
    path('iscrizione_prolunga_method/<int:id>', views.iscrizione_prolunga_method, name='iscrizione-prolunga-method'),
    path('permesso_negato/', views.permesso_negato, name='permesso-negato'),
    path('nuova_scheda/', views.nuova_scheda, name='nuova-scheda'),
    path('elimina_scheda/<int:id>', views.elimina_scheda, name='elimina-scheda'),
    path('dettagli_scheda/<int:id>', views.dettagli_scheda, name='dettagli-scheda'),
    path('cerca_schede/', views.cerca_schede, name='cerca-schede'),
    path('aggiungi_esercizi/<int:id>', views.aggiungi_esercizi, name='aggiungi-esercizi'),
    path('elimina_esericizio/<int:id>', views.elimina_esercizio, name='elimina-esercizio'),
    path('consulta_calendario/<int:id>/', login_required(views.CalendarView.as_view()), name='consulta-calendario'),
    path('prenotazione/<int:pt_id>', views.prenotazione, name='prenotazione'),
]

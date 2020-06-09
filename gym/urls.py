from django.urls import path
from . import views

app_name = "gym"

urlpatterns = [
    path('', views.home, name='home'),
    path('corso_search', views.corso_search, name='corso-search'),
    path('corso_dettagli/<int:id>', views.corso_dettagli, name='corso-dettagli'),
]

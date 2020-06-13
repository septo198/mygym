from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from .urls import *

#Decoratori personalizzati che controllano il ruolo di un utente (usati in views)

#Controlla che l'utente sia un cliente
def cliente_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='gym:permesso-negato'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_cliente,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

#Controllo che l'utente sia un pt
def pt_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='gym:permesso-negato'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_pt,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

#Controllo che l'utente sia un portinaio
def portinaio_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='gym:permesso-negato'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_portinaio,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

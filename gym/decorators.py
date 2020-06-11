from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from .urls import *


def cliente_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='gym:permesso-negato'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_cliente,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def pt_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='gym:permesso-negato'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_pt,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def portinaio_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='gym:permesso-negato'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_portinaio,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

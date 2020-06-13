from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import *


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'is_cliente', 'is_pt', 'is_portinaio', 'foto_profilo', 'password1', 'password2')}
         ),
    )

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("La mail selezionata è già esistente")
        return data


admin.site.register(Cliente)
admin.site.register(Corso)
admin.site.register(Iscrizione)
admin.site.register(Pt)
admin.site.register(Portinaio)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Prenotazione)

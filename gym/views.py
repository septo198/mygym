from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.db.models import Q

# Create your views here.
def home(request):
    corsi = Corso.objects.all()
    context = {'corsi': corsi}
    return render(request, 'gym/home.html', context)


def corso_search(request):
    if request.method == 'POST':
        form = CorsoForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['nome'] == '':
                corsi = Corso.objects.all()
            else:
                corsi = Corso.objects.filter(Q(nome__icontains=form.cleaned_data['nome']))
    else:
        form = CorsoForm
        corsi = Corso.objects.all()
    context = {'form': form, 'corsi': corsi}
    return render(request, 'gym/corso_search.html', context)


def corso_dettagli(request, id):
    corso = Corso.objects.get(id=id)
    context = {'corso': corso}
    return render(request, 'gym/corso_dettagli.html', context)

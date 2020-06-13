import calendar

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django_tables2 import TemplateColumn, RequestConfig
from django.views import generic
from django.utils.safestring import mark_safe

from .forms import *
from .models import *
from .decorators import *
from .utils import *
from django.db.models import Q
from django.contrib.auth import login, user_logged_out
from django.shortcuts import redirect
from django.views.generic import CreateView
import django_tables2 as tables
from datetime import datetime, timedelta, date


def home(request):
    corsi = Corso.objects.all()
    logged_user = request.user
    context = {'corsi': corsi, 'logged_user': logged_user}
    return render(request, 'gym/home.html', context)


def corso_search(request):
    if request.method == 'POST':
        form = CorsoForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['nome'] == '' and form.cleaned_data['prezzo_max'] == 0.0:
                corsi = Corso.objects.all()
            else:
                corsi = Corso.objects.filter(Q(nome__icontains=form.cleaned_data['nome']) & Q(prezzo__lte=form.cleaned_data['prezzo_max']))
    else:
        form = CorsoForm
        corsi = Corso.objects.all()
    logged_user = request.user
    context = {'form': form, 'corsi': corsi, 'logged_user': logged_user}
    return render(request, 'gym/corso_search.html', context)


def corso_dettagli(request, id):
    corso = Corso.objects.get(id=id)
    try:
        iscrizione = Iscrizione.objects.get(cliente=request.user, corso=corso)
    except Iscrizione.DoesNotExist:
        iscrizione = None
    logged_user = request.user
    context = {'corso': corso, 'logged_user': logged_user, 'iscrizione': iscrizione}
    return render(request, 'gym/corso_dettagli.html', context)


class ClienteSignUpView(CreateView):
    model = User
    form_class = ClienteSignUpForm
    template_name = 'gym/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'cliente'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('gym:home')


class PtSignUpView(CreateView):
    model = Pt
    form_class = PtSignUpForm
    template_name = 'gym/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'pt'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('gym:home')


@login_required
def logout(request):
    user = getattr(request, 'user', None)
    user = None
    user_logged_out.send(sender=User.__class__, request=request, user=User)
    request.session.flush()
    if hasattr(request, 'user'):
        request.user = AnonymousUser()
    return redirect('gym:home')


def pt_page(request):
    logged_user = request.user
    context = {'logged_user': logged_user}
    return render(request, 'gym/pt_page.html', context)


def user_login(request):
    return redirect('gym:login')


@login_required()
def utente_details(request, id):
    user = User.objects.get(id=id)
    corsi = Corso.objects.all()
    iscrizioni = Iscrizione.objects.filter(cliente_id=user.id)
    schede = Scheda.objects.filter(autore=user)
    prenotazioni = Prenotazione.objects.all()
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            user.foto_profilo = form.cleaned_data['image']
            user.save()
            return redirect('gym:utente-details', id=id)
    else:
        form = UserUpdateForm()
    logged_user = request.user
    context = {'user': user, 'iscrizioni': iscrizioni, 'corsi': corsi, 'logged_user': logged_user, 'form': form, 'schede': schede}
    return render(request, 'gym/utente_dettagli.html', context)


class ResultsTable(tables.Table):
    class Meta:
        model = User
        template_name = "django_tables2/bootstrap4.html"
        fields = ("first_name", "last_name", "email")
        attrs = {"class": "table table-striped table-bordered sortable",
                 "data-toggle": "table"
                 }

    detail = TemplateColumn(exclude_from_export=False, template_name='gym/button_details.html', orderable=False,
                            verbose_name='')

@login_required()
def ricerca_pt(request):
    pts = User.objects.filter(is_pt=True)
    table = ResultsTable(pts)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['first_name'] == form.cleaned_data['last_name'] == form.cleaned_data['email'] == '':
                pts = pts
            else:
                pts = pts.filter(Q(first_name__icontains=form.cleaned_data['first_name']) & Q(
                    last_name__icontains=form.cleaned_data['last_name']) & Q(
                    email__icontains=form.cleaned_data['email']))
                table = ResultsTable(pts)
    else:
        form = UserSearchForm
    logged_user = request.user
    context = {'pts': pts, 'logged_user': logged_user, 'table': table, 'form': form}
    return render(request, 'gym/ricerca_pt.html', context)


@login_required()
@portinaio_required()
def ricerca_cliente(request):
    clienti = User.objects.filter(is_cliente=True)
    table = ResultsTable(clienti)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['first_name'] == form.cleaned_data['last_name'] == form.cleaned_data['email'] == '':
                clienti = clienti
            else:
                clienti = clienti.filter(Q(first_name__icontains=form.cleaned_data['first_name']) & Q(
                    last_name__icontains=form.cleaned_data['last_name']) & Q(email__icontains=form.cleaned_data['email']))
                table = ResultsTable(clienti)
    else:
        form = UserSearchForm
    logged_user = request.user
    context = {'clienti': clienti, 'logged_user': logged_user, 'table': table, 'form': form}
    return render(request, 'gym/ricerca_cliente.html', context)


@login_required()
@portinaio_required()
def aggiungi_corso(request):
    if request.method == 'POST':
        form = CorsoAddForm(request.POST, request.FILES)
        if form.is_valid():
            corso = form.save(commit=False)
            corso.save()
            return redirect('gym:corso-dettagli', id=corso.id)
    else:
        form = CorsoAddForm()
    logged_user = request.user
    context = {'logged_user': logged_user, 'form': form}
    return render(request, 'gym/aggiungi_corso.html', context)


@login_required()
@cliente_required()
def iscrizione_corso(request, id):
    corso = Corso.objects.get(id=id)
    if request.method == 'POST':
        if corso.posti_rimanenti > 0:
            form = IscrizioneAddForm(request.POST)
            if form.is_valid():
                iscrizione = form.save(commit=False)
                iscrizione.corso_id = corso.id
                iscrizione.cliente_id = request.user.id
                iscrizione.costo_complessivo = iscrizione.mesi_durata * corso.prezzo
                iscrizione.data_iscrizione = datetime.now()
                iscrizione.data_scadenza = datetime.now() + (iscrizione.mesi_durata*timedelta(days=30))
                iscrizione.save()
                corso.iscritti_attuali += 1
                corso.save()
                return redirect('gym:utente-details', id=iscrizione.cliente_id)
        else:
            redirect('gym:iscrizione-corso', id=id)
    else:
        form = IscrizioneAddForm
    logged_user = request.user
    context = {'logged_user': logged_user, 'form': form, 'corso': corso}
    return render(request, 'gym/iscrizione_corso.html', context)


@login_required()
def iscrizione_delete(request, id):
    iscrizione = Iscrizione.objects.get(id=id)
    user = User.objects.get(id=iscrizione.cliente.id)
    corso = Corso.objects.get(id=iscrizione.corso.id)
    corso.iscritti_attuali -= 1
    corso.save()
    iscrizione.delete()
    return redirect('gym:utente-details', user.id)


@login_required()
@portinaio_required()
def elimina_corso(request, id):
    corso = Corso.objects.get(id=id)
    corso.delete()
    return redirect('gym:corso-search')


@login_required()
@portinaio_required()
def salda_iscrizione(request, id):
    iscrizione = Iscrizione.objects.get(id=id)
    cliente = User.objects.get(id=iscrizione.cliente.id)
    iscrizione.pagato = True
    iscrizione.costo_complessivo = 0
    iscrizione.save()
    return redirect('gym:utente-details', cliente.id)


def permesso_negato(request):
    logged_user = request.user
    context = {'logged_user': logged_user}
    return render(request, 'gym/permesso_negato.html', context)


def iscrizione_prolunga_method(request, id):
    iscrizione = Iscrizione.objects.get(id=id)
    user = User.objects.get(id=iscrizione.cliente.id)
    corso = Corso.objects.get(id=iscrizione.corso.id)
    mesi_agg = 0
    if request.method == 'POST':
        if request.POST.get('mesi', False):
            mesi_agg = int(request.POST['mesi'])
            if iscrizione.pagato:
                iscrizione.costo_complessivo = mesi_agg * corso.prezzo
                iscrizione.pagato = False
            else:
                iscrizione.costo_complessivo = iscrizione.costo_complessivo + (mesi_agg * corso.prezzo)
    iscrizione.mesi_durata = iscrizione.mesi_durata + mesi_agg
    iscrizione.data_scadenza = iscrizione.data_iscrizione + (iscrizione.mesi_durata*timedelta(days=30))
    iscrizione.save()
    return redirect('gym:utente-details', user.id)


@login_required()
@pt_required()
def nuova_scheda(request):
    if request.method == 'POST':
        form = SchedaAddForm(request.POST)
        if form.is_valid():
            scheda = form.save(commit=False)
            scheda.autore = request.user
            scheda.save()
            return redirect('gym:aggiungi-esercizi', id=scheda.id)
    else:
        form = SchedaAddForm()
    logged_user = request.user
    context = {'logged_user': logged_user, 'form': form}
    return render(request, 'gym/nuova_scheda.html', context)


@login_required()
@pt_required()
def aggiungi_esercizi(request, id):
    scheda = Scheda.objects.get(id=id)
    esercizi = Esercizio.objects.filter(scheda_id=id)
    if request.method == 'POST':
        form = EsercizioAddForm(request.POST)
        if form.is_valid():
            esercizio = form.save(commit=False)
            esercizio.scheda = scheda
            esercizio.save()
            return redirect('gym:aggiungi-esercizi', id)
    else:
        form = EsercizioAddForm()
    logged_user = request.user
    context = {'logged_user': logged_user, 'scheda': scheda, 'esercizi': esercizi, 'form': form}
    return render(request, 'gym/aggiungi_esercizi.html', context)


@login_required()
@pt_required()
def elimina_esercizio(request, id):
    esercizio = Esercizio.objects.get(id=id)
    esercizio.delete()
    return redirect('gym:aggiungi-esercizi', esercizio.scheda.id)


@login_required()
@pt_required()
def elimina_scheda(request, id):
    scheda = Scheda.objects.get(id=id)
    scheda.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def dettagli_scheda(request, id):
    scheda = Scheda.objects.get(id=id)
    esercizi = Esercizio.objects.filter(scheda_id=id)
    logged_user = request.user
    context = {'logged_user': logged_user, 'scheda': scheda, 'esercizi': esercizi}
    return render(request, 'gym/dettagli_scheda.html', context)


class SchedeTable(tables.Table):
    class Meta:
        model = Scheda
        template_name = "django_tables2/bootstrap4.html"
        fields = ("nome", "autore")
        attrs = {"class": "table table-striped table-bordered sortable",
                 "data-toggle": "table"
                 }

    detail = TemplateColumn(exclude_from_export=False, template_name='gym/apri_scheda.html', orderable=False,
                            verbose_name='', )


@login_required()
def cerca_schede(request):
    schede = Scheda.objects.all()
    table = SchedeTable(schede)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    if request.method == 'POST':
        form = SchedeSearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['nome'] == form.cleaned_data['autore'] == '':
                schede = schede
            else:
                schede = schede.filter(Q(nome__icontains=form.cleaned_data['nome'])&
                                       Q(autore__username__icontains=form.cleaned_data['autore']))
                table = SchedeTable(schede)
    else:
        form = SchedeSearchForm()
    logged_user = request.user
    context = {'logged_user': logged_user, 'schede': schede, 'form': form, 'table': table}
    return render(request, 'gym/cerca_schede.html', context)


class CalendarView(generic.ListView):
    model = Prenotazione
    template_name = 'gym/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        #d = get_date(self.request.GET.get('day', None))

        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['logged_user'] = self.request.user
        context['calendar'] = mark_safe(html_cal)
        context['pt'] = User.objects.get(id=self.kwargs['id'])
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def prenotazione(request, pt_id):
    if request.method == 'POST':
        form = PrenotazioneAddForm(request.POST)
        if form.is_valid():
            prenotazione = form.save(commit=False)
            prenotazione.cliente = Cliente.objects.get(user=request.user)
            prenotazione.pt = Pt.objects.get(user_id=pt_id)
            form.save()
            return redirect('gym:consulta-calendario', id=pt_id)
    else:
        form = PrenotazioneAddForm()
    pt = User.objects.get(id=pt_id)
    logged_user = request.user
    context = {'logged_user': logged_user, 'form': form, 'pt': pt}
    return render(request, 'gym/prenotazione.html', context)

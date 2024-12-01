from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Colis, Profil
from .forms import LoginForm
from django import forms
from django.views.generic.edit import FormView
from .utils import authenticate_by_email

class CustomLoginView(FormView):
    template_name = 'core/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate_by_email(email, password)

        if user is not None:
            login(self.request, user)
            next_url = self.request.POST.get('next', '/')
            return redirect(next_url)
        else:
            form.add_error(None, "Les informations saisies ne correspondent à aucun compte. Veuillez réessayer.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_url = self.request.GET.get('next', '/')

        is_colis_url = next_url.startswith('/colis/')
        next_colis_id = next_url.split('/')[2] if is_colis_url else None

        context['is_colis_url'] = is_colis_url
        context['next_colis_id'] = next_colis_id
        context['next'] = next_url

        return context


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre compte a été créé avec succès !")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

class LoginForm(forms.Form):
    email = forms.EmailField(label="Adresse mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                form.add_error(None, "Adresse mail ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

def test_view(request):
    return render(request, 'core/test.html', {})


@login_required
def account_view(request):
    try:
        profil = Profil.objects.get(utilisateur=request.user)
        jauge_score = (profil.score / 1000) * 100
        jauge_score = min(jauge_score, 100)
        
        # Debug : Affiche les valeurs dans la console
        print(f"Score actuel: {profil.score}, Jauge: {jauge_score}%")
    except Profil.DoesNotExist:
        profil = None
        jauge_score = 0
        print("Aucun profil trouvé pour cet utilisateur.")

    return render(request, 'core/account.html', {
        'profil': profil,
        'jauge_score': jauge_score,
    })

def accueil(request):
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('/')


def scan_colis(request, colis_id):
    colis = get_object_or_404(Colis, id=colis_id)  # Récupère le colis ou affiche une erreur 404
    message_ecologique = colis.calcul_economie_co2()  # Génère un message écologique si applicable
    return render(request, 'core/scan_colis.html', {
        'colis': colis,
        'message_ecologique': message_ecologique,
    })


def retour_colis(request, colis_id):
    colis = get_object_or_404(Colis, id=colis_id)

    if request.method == 'POST':
        if request.user.is_authenticated:
            colis.utilisateur = request.user
            colis.status_retour = 'en_attente'
            colis.save()
            messages.success(request, "Colis marqué comme en attente de validation.")
            return redirect('scan_colis', colis_id=colis_id)
        else:
            messages.error(request, "Veuillez créer un compte pour profiter des avantages d'Opack.")
            return redirect('signup', next=f'/colis/{colis_id}/retour/')

    return render(request, 'core/retour_colis.html', {'colis': colis})


def reutiliser_colis(request, colis_id):
    colis = get_object_or_404(Colis, id=colis_id)
    return render(request, 'core/action_result.html', {'colis': colis, 'message': "Le colis a été marqué comme 'réutilisé'."})


def retourner_vendeur(request, colis_id):
    colis = get_object_or_404(Colis, id=colis_id)
    return render(request, 'core/action_result.html', {'colis': colis, 'message': "Le colis a été marqué comme 'retourné au vendeur'."})

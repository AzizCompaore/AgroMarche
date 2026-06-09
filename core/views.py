from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Annonce, Crop, OfficialPrice, Profil, Favori
from .forms import AnnonceForm, InscriptionForm, ProfilForm


def home(request):
    # On garde les cultures et prix officiels pour l'accueil
    cultures = Crop.objects.all()
    prix_officiels = OfficialPrice.objects.all()

    # LIMITATION : On ne prend que les 6 dernières annonces pour ne pas surcharger l'accueil
    annonces = Annonce.objects.filter(is_active=True).order_by('-date_publication')[:6]

    # Gestion des favoris pour l'utilisateur connecté
    user_favoris_ids = []
    if request.user.is_authenticated:
        user_favoris_ids = Favori.objects.filter(user=request.user).values_list('annonce_id', flat=True)

    return render(request, 'core/home.html', {
        'annonces': annonces,
        'cultures': cultures,
        'prix_officiels': prix_officiels,
        'user_favoris_ids': user_favoris_ids
    })


def liste_annonces(request):
    """ Nouvelle vue pour afficher TOUTES les annonces (Le Marché) """
    culture_nom = request.GET.get('culture')
    cultures = Crop.objects.all()
    annonces = Annonce.objects.filter(is_active=True).order_by('-date_publication')

    if culture_nom:
        annonces = annonces.filter(culture__name=culture_nom)

    user_favoris_ids = []
    if request.user.is_authenticated:
        user_favoris_ids = Favori.objects.filter(user=request.user).values_list('annonce_id', flat=True)

    return render(request, 'core/liste_annonces.html', {
        'annonces': annonces,
        'cultures': cultures,
        'culture_active': culture_nom,
        'user_favoris_ids': user_favoris_ids
    })


def detail_annonce(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk)
    return render(request, 'core/detail_annonce.html', {'annonce': annonce})


@login_required
def creer_annonce(request):
    if hasattr(request.user, 'profil') and request.user.profil.role != 'vendeur':
        return redirect('home')
    if request.method == 'POST':
        form = AnnonceForm(request.POST, request.FILES)
        if form.is_valid():
            annonce = form.save(commit=False)
            annonce.vendeur = request.user
            annonce.save()
            return redirect('home')
    else:
        form = AnnonceForm()
    return render(request, 'core/creer_annonce.html', {'form': form})


@login_required
def mes_annonces(request):
    annonces = Annonce.objects.filter(vendeur=request.user).order_by('-date_publication')
    return render(request, 'core/mes_annonces.html', {'annonces': annonces})


def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            role_choisi = form.cleaned_data.get('role')
            tel_choisi = form.cleaned_data.get('telephone')
            Profil.objects.create(user=user, role=role_choisi, telephone=tel_choisi)
            auth_login(request, user)
            return redirect('home')
    else:
        form = InscriptionForm()
    return render(request, 'core/inscription.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect(request.GET.get('next', 'home'))
    else:
        form = AuthenticationForm()
    return render(request, 'core/connexion.html', {'form': form})


def deconnexion(request):
    auth_logout(request)
    return redirect('home')


@login_required
def supprimer_annonce(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk, vendeur=request.user)
    if request.method == 'POST':
        annonce.delete()
        return redirect('mes_annonces')
    return render(request, 'core/supprimer_confirm.html', {'annonce': annonce})


@login_required
def mon_profil(request):
    profil = request.user.profil
    if request.method == 'POST':
        form = ProfilForm(request.POST, instance=profil)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès !")
            return redirect('mon_profil')
    else:
        form = ProfilForm(instance=profil)
    return render(request, 'core/profil.html', {'form': form, 'profil': profil})


# --- LOGIQUE DES FAVORIS ---

@login_required
def toggle_favori(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    favori, created = Favori.objects.get_or_create(user=request.user, annonce=annonce)
    if not created:
        favori.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def liste_favoris(request):
    mes_favoris = Annonce.objects.filter(favorisé_par__user=request.user)
    return render(request, 'core/favoris.html', {'favoris': mes_favoris})
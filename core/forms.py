from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Annonce
from .models import Profil

class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['culture', 'quantite', 'prix_demande', 'ville', 'description', 'image']
        widgets = {
            'culture': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 500'}),
            'prix_demande': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix total en CFA'}),
            'ville': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Daloa, Soubré...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Détails sur la qualité, disponibilité...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'culture': 'Produit Agricole',
            'quantite': 'Quantité (kg)',
            'prix_demande': 'Prix demandé (CFA)',
            'ville': 'Lieu du stock (Ville/Village)',
        }

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(label="Adresse email", required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(
        label="Type de compte",
        choices=[('vendeur', 'Planteur / Coopérative'), ('acheteur', 'Acheteur / Exportateur')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    telephone = forms.CharField(
        label="Numéro de téléphone (WhatsApp)",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: +225...'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'telephone', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On traduit manuellement les textes d'aide de Django
        if 'username' in self.fields:
            self.fields['username'].help_text = "Obligatoire. 150 caractères ou moins. Lettres, chiffres et @/./+/-/_ uniquement."
            self.fields['username'].label = "Nom d'utilisateur"

class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['telephone', 'ville']
        widgets = {
            'telephone': forms.TextInput(attrs={'placeholder': 'Ex: +225 0707070707'}),
            'ville': forms.TextInput(attrs={'placeholder': 'Votre ville actuelle'}),
        }
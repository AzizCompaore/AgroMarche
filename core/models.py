from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import io
from django.core.files.base import ContentFile


# --- MODÈLE PROFIL ---
class Profil(models.Model):
    CHOIX_ROLE = [
        ('vendeur', 'Planteur / Coopérative'),
        ('acheteur', 'Acheteur / Exportateur'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    role = models.CharField(max_length=20, choices=CHOIX_ROLE, default='vendeur')
    telephone = models.CharField(max_length=15, blank=True)
    ville = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


# --- MODÈLES DE GESTION DES CULTURES ---
class Crop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, default="bi-box")

    def __str__(self):
        return self.name


class OfficialPrice(models.Model):
    crop = models.OneToOneField(Crop, on_delete=models.CASCADE)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prix {self.crop.name}: {self.price_per_kg} CFA"


# --- MODÈLE DES ANNONCES ---
class Annonce(models.Model):
    vendeur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='annonces')
    culture = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(help_text="En kg")
    prix_demande = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='annonces/', blank=True, null=True)
    ville = models.CharField(max_length=100)
    date_publication = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.culture.name} - {self.vendeur.username}"

    def save(self, *args, **kwargs):
        # Compression automatique de l'images
        if self.image:
            img = Image.open(self.image)
            # Conversion en RGB pour JPEG
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Redimensionnement max 1000px
            img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)

            output = io.BytesIO()
            img.save(output, format='JPEG', quality=75)
            output.seek(0)

            # Renommage en .jpg pour l'optimisation
            self.image = ContentFile(output.read(), name=self.image.name.split('.')[0] + '.jpg')

        super().save(*args, **kwargs)

class Favori(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoris')
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='favorisé_par')
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'annonce') # Empêche de mettre deux fois le même favori

    def __str__(self):
        return f"{self.user.username} aime {self.annonce.culture.name}"
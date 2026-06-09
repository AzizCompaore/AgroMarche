from django.contrib import admin
from .models import Crop, OfficialPrice, Annonce

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')

@admin.register(OfficialPrice)
class OfficialPriceAdmin(admin.ModelAdmin):
    list_display = ('crop', 'price_per_kg', 'updated_at')

@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('culture', 'vendeur', 'quantite', 'prix_demande', 'date_publication', 'is_active')
    list_filter = ('culture', 'is_active')
    search_fields = ('ville', 'description')

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('marche/', views.liste_annonces, name='liste_annonces'),  # La nouvelle page pour toutes les annonces
    path('ajouter-stock/', views.creer_annonce, name='creer_annonce'),
    path('annonce/<int:pk>/', views.detail_annonce, name='detail_annonce'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('mes-stocks/', views.mes_annonces, name='mes_annonces'),
    path('annonce/supprimer/<int:pk>/', views.supprimer_annonce, name='supprimer_annonce'),
    path('mon-profil/', views.mon_profil, name='mon_profil'),
    path('favori/toggle/<int:annonce_id>/', views.toggle_favori, name='toggle_favori'),
    path('mes-favoris/', views.liste_favoris, name='liste_favoris'),
]
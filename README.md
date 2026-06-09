AgroMarché
AgroMarché est une plateforme de mise en relation entre planteurs / coopératives agricoles et acheteurs / exportateurs en Côte d'Ivoire. Elle permet aux producteurs de publier leurs stocks de cultures, et aux acheteurs de parcourir le marché, consulter les prix officiels et sauvegarder leurs annonces favorites.
---
Fonctionnalités
Tableau de bord d'accueil — aperçu des 6 dernières annonces publiées et des prix officiels par culture
Marché complet — liste paginable de toutes les annonces, filtrable par type de culture
Publication d'annonces — les vendeurs peuvent créer une annonce avec photo, quantité, prix, ville et description. Les images sont automatiquement compressées et redimensionnées (max 1000 × 1000 px, qualité 75 %)
Gestion de ses stocks — chaque vendeur accède à ses annonces et peut les supprimer
Système de favoris — les acheteurs peuvent mettre en favori/retirer les annonces qui les intéressent
Profil utilisateur — deux rôles distincts (Planteur / Coopérative et Acheteur / Exportateur), numéro WhatsApp et ville modifiables
Authentification complète — inscription, connexion et déconnexion sécurisées
---
Structure du projet
```
agromarche_pro/
├── agromarche_pro/          # Configuration Django (settings, urls, wsgi, asgi)
├── core/                    # Application principale
│   ├── models.py            # Modèles : Profil, Crop, OfficialPrice, Annonce, Favori
│   ├── views.py             # Logique métier et vues
│   ├── urls.py              # Routes de l'application
│   ├── forms.py             # Formulaires : annonce, inscription, profil
│   ├── admin.py             # Interface d'administration
│   ├── templates/core/      # Templates HTML (base, home, marché, détail, profil…)
│   └── static/core/         # Fichiers statiques (logo, images)
├── media/                   # Fichiers uploadés par les utilisateurs
├── manage.py
└── db.sqlite3
```
---
Prérequis
Python 3.10+
pip
---
Installation et lancement
1. Cloner le dépôt
```bash
git clone https://github.com/AzizCompaore/AgroMarche.git
cd AgroMarche
```
2. Créer et activer l'environnement virtuel
```bash
python -m venv .venv
```
Windows :
```bash
.venv\Scripts\activate
```
macOS / Linux :
```bash
source .venv/bin/activate
```
3. Installer les dépendances
```bash
pip install django pillow
```
4. Appliquer les migrations
```bash
python manage.py migrate
```
5. Créer un super-utilisateur (optionnel, pour l'admin)
```bash
python manage.py createsuperuser
```
6. Lancer le serveur de développement
```bash
python manage.py runserver
```
L'application est accessible sur http://127.0.0.1:8000.
L'interface d'administration Django est disponible sur http://127.0.0.1:8000/admin.
---
Routes principales
URL	Nom	Description
`/`	`home`	Page d'accueil
`/marche/`	`liste_annonces`	Toutes les annonces (filtre par culture)
`/annonce/<id>/`	`detail_annonce`	Détail d'une annonce
`/ajouter-stock/`	`creer_annonce`	Publier une annonce (vendeur requis)
`/mes-stocks/`	`mes_annonces`	Gérer ses propres annonces
`/mes-favoris/`	`liste_favoris`	Annonces mises en favori
`/mon-profil/`	`mon_profil`	Modifier son profil
`/inscription/`	`inscription`	Créer un compte
`/connexion/`	`connexion`	Se connecter
`/deconnexion/`	`deconnexion`	Se déconnecter
---
Modèles de données
Modèle	Description
`Profil`	Extension du `User` Django — rôle, téléphone, ville
`Crop`	Catégorie de culture (cacao, cajou, maïs…) avec icône
`OfficialPrice`	Prix officiel par kg pour chaque culture
`Annonce`	Stock mis en vente — culture, quantité, prix, ville, photo
`Favori`	Association utilisateur ↔ annonce
---
Stack technique
Composant	Technologie
Backend	Django 6.0
Base de données	SQLite (développement)
Traitement d'images	Pillow
Frontend	HTML / Bootstrap 5 (templates Django)
Authentification	`django.contrib.auth`
---
Notes de sécurité (production)
Avant tout déploiement en production, penser à :
Passer `DEBUG = False` dans `settings.py`
Remplacer la `SECRET_KEY` par une valeur secrète générée aléatoirement
Configurer une base de données robuste (PostgreSQL recommandé)
Définir `ALLOWED_HOSTS` avec le domaine réel
Servir les fichiers statiques et media via un serveur web (Nginx, etc.)
---
Auteur
Compaoré Abdoul Aziz
GitHub : @AzizCompaore
LinkedIn : aziz-compaore-549337299

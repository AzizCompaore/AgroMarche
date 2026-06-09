🌾 AgroMarché Pro
> Plateforme de mise en relation entre producteurs agricoles et acheteurs en Afrique de l'Ouest.
AgroMarché Pro est une application web qui permet aux planteurs et coopératives de publier leurs stocks agricoles, et aux acheteurs / exportateurs de consulter les offres disponibles, le tout en temps réel et en FCFA.
---
✨ Fonctionnalités
Pour les vendeurs (Planteurs / Coopératives)
📢 Publier une annonce de stock (culture, quantité, prix, ville, photo)
📋 Consulter et gérer ses propres annonces
🗑️ Supprimer une annonce
Pour les acheteurs (Acheteurs / Exportateurs)
🛒 Parcourir le marché et filtrer les annonces par culture
❤️ Sauvegarder des annonces en favoris
📞 Contacter le vendeur via son numéro WhatsApp
Pour tous
💰 Consulter les prix officiels de référence par culture (en FCFA/kg)
👤 Créer un compte avec un rôle défini (vendeur ou acheteur)
✏️ Modifier son profil (téléphone, ville)
---
🌱 Cultures supportées
Noix de cajou · Cacao · Café · Caoutchouc · Arachides · Maïs · Sorgho · Coton · et autres cultures de rente
---
🛠️ Stack technique
Composant	Technologie
Backend	Python 3 / Django
Base de données	SQLite (développement)
Frontend	Bootstrap 5 + Django Templates
Traitement images	Pillow (compression automatique)
Authentification	Django Auth intégré
Langue	Français (`fr-fr`)
---
🚀 Installation
Prérequis
Python 3.10+
pip
Étapes
```bash
# 1. Cloner le dépôt
git clone https://github.com/ton-username/agromarche-pro.git
cd agromarche_pro

# 2. Créer et activer l'environnement virtuel
python -m venv .venv

# Sur Linux / macOS
source .venv/bin/activate

# Sur Windows
.venv\Scripts\activate

# 3. Installer les dépendances
pip install django pillow

# 4. Appliquer les migrations
python manage.py migrate

# 5. (Optionnel) Créer un super-utilisateur pour l'admin
python manage.py createsuperuser

# 6. Lancer le serveur de développement
python manage.py runserver
```
L'application est accessible à : http://127.0.0.1:8000
L'interface d'administration Django est accessible à : http://127.0.0.1:8000/admin
---
📁 Structure du projet
```
agromarche_pro/
│
├── agromarche_pro/          # Configuration du projet Django
│   ├── settings.py          # Paramètres (BDD, médias, langue...)
│   ├── urls.py              # Routage principal
│   ├── wsgi.py
│   └── asgi.py
│
├── core/                    # Application principale
│   ├── models.py            # Modèles : Profil, Crop, OfficialPrice, Annonce, Favori
│   ├── views.py             # Vues : accueil, marché, annonces, favoris, profil
│   ├── forms.py             # Formulaires : inscription, annonce, profil
│   ├── urls.py              # Routes de l'application
│   ├── admin.py             # Interface d'administration
│   ├── migrations/          # Migrations de la base de données
│   ├── templates/core/      # Templates HTML
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── liste_annonces.html
│   │   ├── detail_annonce.html
│   │   ├── creer_annonce.html
│   │   ├── mes_annonces.html
│   │   ├── favoris.html
│   │   ├── profil.html
│   │   ├── inscription.html
│   │   └── connexion.html
│   └── static/core/         # Images et fichiers statiques
│
├── media/                   # Fichiers uploadés par les utilisateurs
│   └── annonces/
│
└── manage.py
```
---
🗄️ Modèles de données
Modèle	Description
`Profil`	Extension du `User` Django avec rôle, téléphone, ville
`Crop`	Culture agricole (nom + icône Bootstrap)
`OfficialPrice`	Prix officiel de référence par culture (FCFA/kg)
`Annonce`	Stock mis en vente par un vendeur
`Favori`	Association unique entre un acheteur et une annonce
---
🖼️ Optimisation des images
Les photos uploadées avec les annonces sont automatiquement :
Redimensionnées à 1000×1000 px maximum
Converties en JPEG
Compressées à 75% de qualité
Cela réduit significativement le poids des fichiers tout en conservant une qualité visuelle satisfaisante.
---
🔒 Gestion des accès
La publication d'annonces est réservée aux utilisateurs avec le rôle vendeur
La consultation du marché et des détails d'annonces est accessible à tous
Les favoris, le profil et la gestion des stocks nécessitent d'être connecté
---

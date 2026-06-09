# 🚇 KONEKT — Métro d'Abidjan

Plateforme web de réservation de billets pour le réseau de métro d'Abidjan (Ligne 1 : Anyama ↔ Aéroport FHB Port-Bouët). Développée avec Django, elle permet aux voyageurs d'acheter des tickets en ligne avec génération de QR code, et offre un tableau de bord de supervision pour les agents.

\---

## ✨ Fonctionnalités

### Côté Voyageur

* **Recherche de trajets** : sélection de la gare de départ et d'arrivée, affichage des prochains départs disponibles
* **Calcul tarifaire dynamique** : le prix est calculé selon le nombre de zones traversées (200 à 800 FCFA)
* **Calcul d'heure de passage** : l'heure affichée correspond à l'heure de passage réelle à la gare choisie (décalage de 3 min par escale)
* **Réservation en ligne** : formulaire passager avec choix du mode de paiement (Orange Money, MTN MoMo, Wave)
* **Ticket numérique** : billet PDF imprimable avec QR code unique généré à la réservation
* **Historique des voyages** : espace personnel listant tous les tickets achetés
* **Carte interactive Leaflet** : visualisation du tracé de la Ligne 1 avec le segment du trajet mis en surbrillance

### Côté Agent / Administration

* **Dashboard de supervision** : nombre total de billets émis, revenu global, activité récente
* **Graphique 7 jours** : volume de réservations sur la dernière semaine
* **Recherche de ticket** : vérification d'un billet par son code
* **Scan QR Code** : validation ou invalidation d'un billet à l'embarquement via l'URL de scan

\---

## 🗂️ Structure du projet

```
Metro\_Abidjan/
├── konekt\_project/          # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── transport/               # Application principale
│   ├── models.py            # Commune, Gare, Voyage, Reservation
│   ├── views.py             # Toutes les vues
│   ├── urls.py              # Routes de l'application
│   ├── admin.py             # Interface d'administration
│   ├── migrations/          # Migrations de base de données
│   └── templates/
│       └── transport/
│           ├── home.html          # Page d'accueil + recherche
│           ├── resultats.html     # Résultats de recherche
│           ├── form\_passager.html # Formulaire de réservation
│           ├── ticket.html        # Billet numérique
│           ├── mes\_tickets.html   # Historique voyageur
│           ├── agent\_dashboard.html # Dashboard agent
│           ├── scan\_result.html   # Résultat de scan QR
│           ├── login.html
│           └── inscription.html
├── static/
│   └── images/              # Images statiques du site
├── media/
│   └── qr\_codes/            # QR codes générés
├── db.sqlite3               # Base de données SQLite
└── manage.py
```

\---

## ⚙️ Installation

### Prérequis

* Python 3.10+
* pip

### 1\. Cloner / extraire le projet

```bash
cd Metro\_Abidjan
```

### 2\. Créer un environnement virtuel

```bash
python -m venv venv

# Windows
venv\\Scripts\\activate

# macOS / Linux
source venv/bin/activate
```

### 3\. Installer les dépendances

```bash
pip install django qrcode\[pil] Pillow
```

### 4\. Appliquer les migrations

```bash
python manage.py migrate
```

### 5\. Créer un superutilisateur (admin)

```bash
python manage.py createsuperuser
```

### 6\. Lancer le serveur

```bash
python manage.py runserver
```

Le site est accessible sur **http://127.0.0.1:8000/**

\---

## 🌐 Routes principales

|URL|Vue|Description|
|-|-|-|
|`/`|`accueil`|Page d'accueil et recherche de trajets|
|`/reserver/<id>/`|`reserver\_etape\_1`|Formulaire passager|
|`/valider/<id>/`|`valider\_reservation`|Confirmation et génération du ticket|
|`/ticket/<code>/`|`voir\_ticket`|Affichage d'un ticket|
|`/mes-tickets/`|`mes\_tickets`|Historique des réservations (connecté)|
|`/scan/<code>/`|`valider\_ticket\_scan`|Validation QR code par l'agent|
|`/agent-control/`|`dashboard\_agent`|Dashboard de supervision (staff)|
|`/login/`|`login\_view`|Connexion|
|`/inscription/`|`inscription\_view`|Création de compte|
|`/admin/`|Django Admin|Gestion complète des données|

\---

## 🗃️ Modèles de données

### `Commune`

Représente une commune sur la ligne (ordonnée par `position`).

|Champ|Type|Description|
|-|-|-|
|`nom`|CharField|Nom de la commune|
|`position`|PositiveIntegerField|Ordre sur la ligne (unique)|

### `Gare`

Station du réseau, rattachée à une commune.

|Champ|Type|Description|
|-|-|-|
|`nom`|CharField|Nom de la gare|
|`commune`|ForeignKey|Commune de rattachement|

### `Voyage`

Départ planifié sur la ligne.

|Champ|Type|Description|
|-|-|-|
|`sens`|CharField|`ALLER` (Anyama→Port-Bouët) ou `RETOUR`|
|`jour\_depart`|DateField|Date du départ|
|`heure\_depart`|TimeField|Heure de départ au terminus|
|`est\_ouvert`|BooleanField|Ouvert à la réservation|
|`gare\_depart\_defaut`|ForeignKey|Terminus de départ (auto-rempli)|
|`gare\_arrivee\_defaut`|ForeignKey|Terminus d'arrivée (auto-rempli)|

### `Reservation`

Ticket acheté par un passager.

|Champ|Type|Description|
|-|-|-|
|`voyage`|ForeignKey|Voyage associé|
|`nom\_passager`|CharField|Nom|
|`prenom\_passager`|CharField|Prénom|
|`gare\_depart\_nom`|CharField|Nom de la gare de départ|
|`gare\_arrivee\_nom`|CharField|Nom de la gare d'arrivée|
|`code\_ticket`|CharField|Code unique (ex: `KNEKT-AF92`)|
|`prix\_paye`|PositiveIntegerField|Montant en FCFA|
|`mode\_paiement`|CharField|Orange / MTN / Wave|
|`heure\_reelle\_passage`|TimeField|Heure de passage calculée à la gare choisie|
|`qr\_code`|ImageField|Image du QR code généré|
|`est\_valide`|BooleanField|`True` = ticket non encore utilisé|
|`date\_utilisation`|DateTimeField|Horodatage du passage en contrôle|

\---

## 🔐 Accès et rôles

|Rôle|Accès|
|-|-|
|**Visiteur**|Recherche, consultation des horaires, achat de tickets sans compte|
|**Voyageur connecté**|+ Historique des tickets (`/mes-tickets/`)|
|**Agent (is\_staff)**|+ Dashboard de supervision, validation des QR codes|
|**Superadmin**|+ Interface `/admin/` complète|

\---

## 🧮 Logique tarifaire

Le prix est calculé selon le nombre de zones (positions de communes) séparant le départ de l'arrivée :

|Zones traversées|Tarif|
|-|-|
|0 – 1|200 FCFA|
|2|300 FCFA|
|3|400 FCFA|
|4|500 FCFA|
|5|600 FCFA|
|6+|800 FCFA|

\---

## 🗺️ Ligne 1 — Stations

La Ligne 1 relie **Anyama Centre** à **l'Aéroport FHB Port-Bouët** en 18 stations sur \~37 km, traversant : Anyama, Abobo, Adjamé, le Plateau, Treichville, Marcory, Koumassi et Port-Bouët.

\---

## 🛠️ Technologies utilisées

|Technologie|Usage|
|-|-|
|**Django 6.0**|Framework web backend|
|**SQLite**|Base de données (développement)|
|**Tailwind CSS** (CDN)|Styles et mise en page|
|**Leaflet.js**|Carte interactive du tracé|
|**Chart.js**|Graphique du dashboard agent|
|**qrcode\[pil]**|Génération des QR codes|
|**Font Awesome**|Icônes|

\---

## 👥 Auteurs

Développé par **Aziz Compaoré**   
© 2026 KONEKT Métro Abidjan


# AgroMarché

AgroMarché met en relation les producteurs agricoles de Côte d'Ivoire et les acheteurs. Le dépôt contient l'application Django d'origine ainsi que ses templates HTML, conservés pour produire une version statique publiable sur GitHub Pages.

## GitHub Pages

Le workflow `.github/workflows/pages.yml` génère le site à partir des templates existants de `core/templates/core/` et publie le résultat après chaque push sur `main`.

Pour activer la publication dans GitHub : ouvrez **Settings → Pages**, puis choisissez **GitHub Actions** comme source de déploiement. Le site publié reprend l'interface actuelle ; les annonces affichées sont des exemples et les images du dossier `media/` sont incluses.

Pour générer le site localement :

```bash
python -m pip install -r requirements-pages.txt
python static_site/build.py
```

Le résultat est créé dans `_site/`. Ouvrez `_site/index.html` ou servez ce dossier avec un serveur de fichiers statiques.

GitHub Pages n'exécute pas Django : les comptes, formulaires, publications, favoris enregistrés côté serveur et données de la base ne sont donc pas fonctionnels sur cette version. Les formulaires affichent un message explicatif au lieu d'échouer. Le site statique utilise des annonces de démonstration ; aucune donnée de la base locale n'est exportée.

## Application Django

Pour exécuter la version avec backend, installez les dépendances de `requirements.txt`, appliquez les migrations, puis lancez :

```bash
python manage.py migrate
python manage.py runserver
```

from __future__ import annotations

import shutil
from datetime import datetime
from html.parser import HTMLParser
from os.path import relpath
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_site"
import sys

sys.path.insert(0, str(ROOT))

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agromarche_pro.settings")

import django

django.setup()

from django.template.loader import render_to_string
from django.test import RequestFactory
from django.urls import resolve
from django.utils.html import mark_safe


class StaticField:
    def __init__(self, name: str, label: str, html: str, help_text: str = "") -> None:
        self.name = name
        self.label = label
        self.html = mark_safe(html)
        self.help_text = help_text
        self.errors = []

    def __html__(self) -> str:
        return str(self.html)

    def __str__(self) -> str:
        return str(self.html)


class StaticForm:
    def __init__(self, fields: list[StaticField]) -> None:
        self.fields = fields
        self.non_field_errors = []
        for field in fields:
            setattr(self, field.name, field)

    def __iter__(self):
        return iter(self.fields)


class StaticPaths(HTMLParser):
    def __init__(self, page_path: Path) -> None:
        super().__init__(convert_charrefs=False)
        self.page_path = page_path
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        rewritten = [(key, self.rewrite(key, value)) for key, value in attrs]
        self.parts.append(f"<{tag}{self.attributes(rewritten)}>")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        rewritten = [(key, self.rewrite(key, value)) for key, value in attrs]
        self.parts.append(f"<{tag}{self.attributes(rewritten)} />")

    def handle_endtag(self, tag: str) -> None:
        self.parts.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def handle_entityref(self, name: str) -> None:
        self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.parts.append(f"&#{name};")

    def handle_comment(self, data: str) -> None:
        self.parts.append(f"<!--{data}-->")

    def handle_decl(self, decl: str) -> None:
        self.parts.append(f"<!{decl}>")

    def handle_pi(self, data: str) -> None:
        self.parts.append(f"<?{data}>")

    def attributes(self, attrs: list[tuple[str, str | None]]) -> str:
        result = []
        for key, value in attrs:
            if value is None:
                result.append(key)
            else:
                escaped = value.replace("&", "&amp;").replace('"', "&quot;")
                result.append(f'{key}="{escaped}"')
        return "".join(f" {attribute}" for attribute in result)

    def rewrite(self, key: str, value: str | None) -> str | None:
        if not value or key not in {"href", "src", "action"}:
            return value

        decoded = unquote(value)
        if decoded.startswith("/static/") or decoded.startswith("/media/"):
            return self.relative_url(OUTPUT / decoded.lstrip("/"))
        if decoded.startswith("static/") or decoded.startswith("media/"):
            return self.relative_url(OUTPUT / decoded)

        if decoded.startswith("/"):
            route = decoded.strip("/")
            if route.startswith("favori/toggle/"):
                return "#"
            if route == "deconnexion":
                route = "connexion"
            target = OUTPUT / route / "index.html" if route else OUTPUT / "index.html"
            return self.relative_url(target) + ("#" if decoded.endswith("/") and route else "")
        return value

    def relative_url(self, target: Path) -> str:
        page_dir = OUTPUT / self.page_path.parent
        return Path(relpath(target, page_dir)).as_posix()


def field(
    name: str,
    label: str,
    input_type: str = "text",
    classes: str = "form-control",
    help_text: str = "",
    **attrs: str,
) -> StaticField:
    extra = "".join(f' {key.replace("_", "-")}="{value}"' for key, value in attrs.items())
    return StaticField(name, label, f'<input type="{input_type}" name="{name}" class="{classes}"{extra}>', help_text)


def make_listing(identifier: int, crop: str, quantity: int, price: int, city: str, seller: str, image: str, phone: str):
    profile = SimpleNamespace(telephone=phone, role="vendeur")
    vendor = SimpleNamespace(username=seller, profil=profile, get_full_name=lambda: seller.title())
    return SimpleNamespace(
        id=identifier,
        pk=identifier,
        culture=SimpleNamespace(name=crop),
        vendeur=vendor,
        quantite=quantity,
        prix_demande=price,
        ville=city,
        description=f"{crop} de qualité, récolté récemment et disponible à {city}. Contactez le vendeur pour organiser la livraison.",
        image=SimpleNamespace(url=f"/media/annonces/{image}"),
        date_publication=datetime(2026, 11, 1),
        is_active=True,
    )


def build() -> None:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)

    listings = [
        make_listing(1, "Cacao", 1200, 1850, "Soubré", "Kouassi", "Les-feves-sechent.jpg", "+2250701020304"),
        make_listing(2, "Noix de cajou", 800, 950, "Korhogo", "Aminata", "noix_de_cajou_icoast_0.jpg", "+2250506070809"),
        make_listing(3, "Maïs", 2500, 400, "Bouaké", "Yao", "pngtree-corn-harvested-in-the-autumn-field-picture-image_1555133.jpg", "+2250102030405"),
        make_listing(4, "Café", 600, 1250, "Man", "Adjoua", "images.jpg", "+2250708091011"),
        make_listing(5, "Caoutchouc", 3000, 720, "Dabou", "N'Guessan", "21450090-raw-rubber-store-in-the-warehouse.jpg", "+2250105090807"),
        make_listing(6, "Arachide", 450, 650, "Daloa", "Fatou", "arachides-el-oued.jpg", "+2250504040302"),
    ]
    crops = [SimpleNamespace(name=name) for name in ("Cacao", "Noix de cajou", "Maïs", "Café", "Caoutchouc", "Arachide")]
    prices = [
        SimpleNamespace(crop=crops[0], price_per_kg=1800),
        SimpleNamespace(crop=crops[1], price_per_kg=950),
        SimpleNamespace(crop=crops[2], price_per_kg=400),
        SimpleNamespace(crop=crops[3], price_per_kg=1250),
    ]

    seller = SimpleNamespace(
        username="Kouassi",
        date_joined=datetime(2025, 5, 12),
        profil=SimpleNamespace(role="vendeur", telephone="+2250701020304", ville="Soubré", get_role_display=lambda: "Planteur / Coopérative"),
        is_authenticated=True,
    )
    buyer = SimpleNamespace(
        username="Aminata",
        date_joined=datetime(2025, 8, 20),
        profil=SimpleNamespace(role="acheteur", telephone="+2250506070809", ville="Abidjan", get_role_display=lambda: "Acheteur / Exportateur"),
        is_authenticated=True,
    )
    anonymous = SimpleNamespace(is_authenticated=False)

    listing_form = StaticForm([
        StaticField("culture", "Produit Agricole", '<select name="culture" class="form-select form-select-lg">' + "".join(f'<option>{crop.name}</option>' for crop in crops) + "</select>"),
        field("ville", "Lieu du stock (Ville/Village)", placeholder="Ex: Daloa, Soubré..."),
        field("quantite", "Quantité (kg)", "number", placeholder="Ex: 500"),
        field("prix_demande", "Prix demandé (CFA)", "number", placeholder="Prix total en CFA"),
        field("image", "Photo du produit", "file"),
        StaticField("description", "Description", '<textarea name="description" class="form-control" rows="3" placeholder="Détails sur la qualité, disponibilité..."></textarea>'),
    ])
    signup_form = StaticForm([
        field("username", "Nom d'utilisateur", help_text="Obligatoire. Nom public affiché sur vos annonces."),
        field("password1", "Mot de passe", "password"),
        field("password2", "Confirmation du mot de passe", "password"),
        field("email", "Adresse email", "email"),
        field("telephone", "Numéro de téléphone (WhatsApp)", placeholder="Ex: +225..."),
        StaticField("role", "Type de compte", '<select name="role" class="form-select"><option value="vendeur">Planteur / Coopérative</option><option value="acheteur">Acheteur / Exportateur</option></select>'),
    ])
    profile_form = StaticForm([
        field("telephone", "Numéro de téléphone", placeholder="Ex: +225 0707070707"),
        field("ville", "Ville de résidence", placeholder="Votre ville actuelle"),
    ])

    pages = [
        ("index.html", "core/home.html", {"annonces": listings[:4], "cultures": crops, "prix_officiels": prices, "user_favoris_ids": [], "user": anonymous}),
        ("marche/index.html", "core/liste_annonces.html", {"annonces": listings, "cultures": crops, "culture_active": "", "user_favoris_ids": [], "user": anonymous}),
        ("ajouter-stock/index.html", "core/creer_annonce.html", {"form": listing_form, "user": seller}),
        ("inscription/index.html", "core/inscription.html", {"form": signup_form, "user": anonymous}),
        ("connexion/index.html", "core/connexion.html", {"user": anonymous}),
        ("deconnexion/index.html", "core/connexion.html", {"user": anonymous}),
        ("mes-stocks/index.html", "core/mes_annonces.html", {"annonces": listings[:3], "user": seller}),
        ("mon-profil/index.html", "core/profil.html", {"form": profile_form, "profil": seller.profil, "user": seller}),
        ("mes-favoris/index.html", "core/favoris.html", {"favoris": listings[1:4], "user": buyer}),
    ]
    pages.extend(
        (f"annonce/supprimer/{listing.pk}/index.html", "core/supprimer_confirm.html", {"annonce": listing, "user": seller})
        for listing in listings[:3]
    )
    pages.extend(
        (f"annonce/{listing.pk}/index.html", "core/detail_annonce.html", {"annonce": listing, "user": anonymous})
        for listing in listings
    )

    request_factory = RequestFactory()
    for relative_path, template_name, context in pages:
        destination = Path(relative_path)
        page_path = OUTPUT / destination
        page_path.parent.mkdir(parents=True, exist_ok=True)
        request = request_factory.get("/" + relative_path.removesuffix("index.html"))
        request.user = context["user"]
        request._messages = []
        request.resolver_match = resolve(request.path)
        html = render_to_string(template_name, context, request=request)
        parser = StaticPaths(destination)
        parser.feed(html)
        result = "".join(parser.parts).replace("</body>", '<script src="' + StaticPaths(destination).relative_url(OUTPUT / "static" / "pages-demo.js") + '"></script></body>')
        page_path.write_text(result, encoding="utf-8")

    static_root = ROOT / "core" / "static"
    if static_root.exists():
        shutil.copytree(static_root, OUTPUT / "static", dirs_exist_ok=True)
    media_root = ROOT / "media"
    if media_root.exists():
        shutil.copytree(media_root, OUTPUT / "media", dirs_exist_ok=True)

    (OUTPUT / "static" / "pages-demo.js").write_text(
        """document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('a[href="#"]').forEach((link) => {
    if (link.closest(".position-absolute")) {
      link.addEventListener("click", (event) => {
        event.preventDefault();
        const icon = link.querySelector("i");
        if (icon) {
          icon.classList.toggle("bi-heart");
          icon.classList.toggle("bi-heart-fill");
          icon.classList.toggle("text-danger");
        }
      });
    }
  });
  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      let notice = form.querySelector("[data-static-notice]");
      if (!notice) {
        notice = document.createElement("div");
        notice.dataset.staticNotice = "true";
        notice.className = "alert alert-info border-0 rounded-3 mt-3";
        form.prepend(notice);
      }
      notice.textContent = "Cette version GitHub Pages est une démonstration statique : les données ne sont pas envoyées ni enregistrées sur le serveur.";
    });
  });
});
""",
        encoding="utf-8",
    )
    (OUTPUT / ".nojekyll").touch()
    print(f"Site statique généré dans {OUTPUT}")


if __name__ == "__main__":
    build()

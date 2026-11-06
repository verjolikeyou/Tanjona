# -*- coding: utf-8 -*-
"""Programme scolaire de 11e — version Toga optimisée.
"""

from __future__ import annotations

import base64
import html as html_lib
import json
import re
import sys
import traceback
from html.parser import HTMLParser
from xml.sax.saxutils import escape

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER

# Données structurées en dictionnaires Python natifs (plus d'erreur JSON.loads)
MENUS = {
    "home": {
        "title": "Programme en 11e",
        "options": ["Français", "Mathématiques", "Cours", "Méthode Boscher"],
        "routes": {
            "Français": "program_fr",
            "Mathématiques": "program_math",
            "Cours": "cours",
            "Méthode Boscher": "methode_boscher"
        },
        "back": None
    },
    "program_fr": {
        "title": "Français — Leçons ou exercices",
        "options": ["Leçons", "Exercices"],
        "routes": {"Leçons": "fr_lecons", "Exercices": "fr_exercices"},
        "back": "home"
    },
    "program_math": {
        "title": "Mathématiques — Leçons ou exercices",
        "options": ["Leçons", "Exercices"],
        "routes": {"Leçons": "math_lecons", "Exercices": "math_exercices"},
        "back": "home"
    },
    "methode_boscher": {
        "title": "Méthode Boscher — Choisissez une leçon",
        "options": ["i - u", "o - a", "e", "p", "t", "r", "n", "m", "l", "c", "d", "v", "s", "b", "f", "j", "g", "ch", "ou", "on", "oi", "an", "in", "br", "fr", "bl", "cl", "ar", "al", "en"],
        "routes": {
            "i - u": "boscher_iu", "o - a": "boscher_oa", "e": "boscher_e", "p": "boscher_p",
            "t": "boscher_t", "r": "boscher_r", "n": "boscher_n", "m": "boscher_m",
            "l": "boscher_l", "c": "boscher_c", "d": "boscher_d", "v": "boscher_v",
            "s": "boscher_s", "b": "boscher_b", "f": "boscher_f", "j": "boscher_j",
            "g": "boscher_g", "ch": "boscher_ch", "ou": "boscher_ou", "on": "boscher_on",
            "oi": "boscher_oi", "an": "boscher_an", "in": "boscher_in", "br": "boscher_br",
            "fr": "boscher_fr", "bl": "boscher_bl", "cl": "boscher_cl", "ar": "boscher_ar",
            "al": "boscher_al", "en": "boscher_en"
        },
        "back": "home"
    },
    "cours": {
        "title": "Cours — Choisissez une leçon",
        "options": ["1-Pose et effectue", "1-Décompose"],
        "routes": {"1-Pose et effectue": "cours_pose_effectue", "1-Décompose": "cours_decompose"},
        "back": "home"
    }
    # Ajoutez vos autres menus ici...
}

CONTENT = {
    "boscher_iu": {
        "kind": "html",
        "title": "Boscher Iu",
        "html": """
        <html><body style="font-family:'Comic Sans MS',sans-serif; text-align:center;">
            <p><span style="background:#0284C7; color:#fff; font-size:15pt; font-weight:bold; padding:6px 16px; border-radius:12px;">Méthode Boscher</span></p>
            <p style="font-size:18pt; font-weight:900; color:#D90429; margin-top:8px;">La rue à midi.</p>
            <p style="font-size:26pt; font-weight:900; color:#E11D48; letter-spacing:8px;">i &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; u</p>
        </body></html>
        """,
        "back": "methode_boscher"
    }
    # Ajoutez vos autres contenus ici...
}

BG = "#F4FBFF"
INK = "#24324A"
PINK = "#FF2E93"
BLUE = "#4361EE"
CYAN = "#80DEEA"
GREEN = "#16804A"


class HTMLVersTexte(HTMLParser):
    BLOCS = {"p", "div", "br", "table", "tr", "ul", "ol", "li", "h1", "h2", "h3", "blockquote"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.in_table_cell = False

    def handle_starttag(self, tag, attrs):
        if tag == "br":
            self.parts.append("\n")
        elif tag == "li":
            self.parts.append("\n• ")
        elif tag in {"td", "th"}:
            if self.in_table_cell:
                self.parts.append("  |  ")
            self.in_table_cell = True
        elif tag in self.BLOCS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"td", "th"}:
            self.in_table_cell = True
        elif tag in self.BLOCS:
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)


def html_en_texte(source: str) -> str:
    try:
        parser = HTMLVersTexte()
        parser.feed(source)
        text = "".join(parser.parts).replace("\xa0", " ")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r" *\n *", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
    except Exception:
        return source


class Programme11eme(toga.App):
    def startup(self):
        try:
            self.state = {"route": "home", "subject": None}
            self.main_window = toga.MainWindow(title="Programme en 11e — Français et Mathématiques")
            self.render()
            self.main_window.show()
        except Exception as e:
            print("ERREUR AU LANCEMENT :", e, file=sys.stderr)
            traceback.print_exc()
            raise e

    def navigate(self, target):
        if target == "program_fr":
            self.state["subject"] = "Français"
        elif target == "program_math":
            self.state["subject"] = "Mathématiques"
        self.state["route"] = target
        self.render()

    def back_to_parent(self, target):
        if target == "program":
            target = "program_math" if self.state.get("subject") == "Mathématiques" else "program_fr"
        elif target == "home":
            self.state["subject"] = None
        self.navigate(target)

    def make_button(self, label, target=None, primary=False, back_target=None):
        if back_target is not None:
            callback = lambda widget: self.back_to_parent(back_target)
        else:
            callback = lambda widget: self.navigate(target)

        return toga.Button(
            label,
            on_press=callback,
            style=Pack(
                margin=8,
                width=500,
                height=50,
                background_color="#4CC9F0" if primary else "#FFFFFF",
                color="#FFFFFF" if primary else PINK,
                font_size=14,
            ),
        )

    def make_label(self, text, size=14, color=INK, bold=False, padding=4):
        return toga.Label(
            text,
            style=Pack(
                margin=padding,
                font_size=size,
                color=color,
                font_weight="bold" if bold else "normal",
                text_align=CENTER,
            ),
        )

    def render_menu(self, route):
        data = MENUS.get(route, MENUS["home"])
        title = data["title"]
        content = toga.Box(style=Pack(direction=COLUMN, flex=1, margin=16, background_color=BG))
        content.add(self.make_label(title, size=22, color="#D90429", bold=True, padding=10))

        buttons_box = toga.Box(style=Pack(direction=COLUMN, flex=1, margin=(4, 8)))
        for label in data["options"]:
            target = data["routes"].get(label)
            if target:
                buttons_box.add(self.make_button(label, target=target, primary=(route == "home")))

        if data.get("back"):
            buttons_box.add(self.make_button("← Retour", back_target=data["back"]))

        scroll = toga.ScrollContainer(content=buttons_box, style=Pack(flex=1))
        content.add(scroll)
        content_box = content
        return content_box

    def render_content(self, route):
        data = CONTENT.get(route, {"kind": "html", "html": "<p>Contenu non disponible</p>", "back": "home"})
        back = data.get("back", "home")
        heading = data.get("title") or route.replace("_", " ").title()

        root = toga.Box(style=Pack(direction=COLUMN, flex=1, margin=12, background_color=BG))
        root.add(self.make_label(heading, size=20, color=PINK, bold=True, padding=8))

        lesson_text = html_en_texte(data.get("html", ""))
        lesson_label = toga.Label(
            lesson_text or "Aucun contenu disponible.",
            style=Pack(margin=16, font_size=14, color=INK),
        )
        content_view = toga.ScrollContainer(
            content=lesson_label,
            style=Pack(flex=1, margin=6, background_color="#FFFFFF"),
        )

        root.add(content_view)
        root.add(self.make_button("← Revenir", back_target=back))
        return root

    def render(self):
        route = self.state["route"]
        if route in MENUS:
            view = self.render_menu(route)
        elif route in CONTENT:
            view = self.render_content(route)
        else:
            view = toga.Box(style=Pack(direction=COLUMN, flex=1, margin=20, align_items=CENTER, justify_content=CENTER))
            view.add(self.make_label("Cette page n’a pas été trouvée.", size=20, color="#B91C1C", bold=True))
            view.add(self.make_button("← Accueil", back_target="home"))
        self.main_window.content = view


def main():
    return Programme11eme("Programme en 11e", "org.verjolikeyou.helloworld")


if __name__ == "__main__":
    main().main_loop()

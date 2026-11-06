# -*- coding: utf-8 -*-
"""Programme scolaire de 11e — version Flask optimisée.
"""

from __future__ import annotations

import sys
import traceback
from flask import Flask, render_template_string, redirect, url_for

app = Flask(__name__)

# Données structurées en dictionnaires Python natifs
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
}

CONTENT = {
    "boscher_iu": {
        "kind": "html",
        "title": "Boscher Iu",
        "html": """
        <div style="font-family:'Comic Sans MS',sans-serif; text-align:center;">
            <p><span style="background:#0284C7; color:#fff; font-size:15pt; font-weight:bold; padding:6px 16px; border-radius:12px;">Méthode Boscher</span></p>
            <p style="font-size:18pt; font-weight:900; color:#D90429; margin-top:8px;">La rue à midi.</p>
            <p style="font-size:26pt; font-weight:900; color:#E11D48; letter-spacing:8px;">i &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; u</p>
        </div>
        """,
        "back": "methode_boscher"
    }
}

BG = "#F4FBFF"
INK = "#24324A"
PINK = "#FF2E93"
BLUE = "#4361EE"
CYAN = "#80DEEA"
GREEN = "#16804A"

TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Programme en 11e — Français et Mathématiques</title>
    <style>
        body {
            background-color: {{ BG }};
            color: {{ INK }};
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background: #FFFFFF;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            width: 100%;
            max-width: 600px;
            text-align: center;
        }
        h1 {
            color: #D90429;
            font-size: 24px;
            margin-bottom: 20px;
        }
        .btn-container {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 20px;
        }
        .btn {
            display: block;
            width: 100%;
            padding: 14px;
            border-radius: 8px;
            text-decoration: none;
            font-size: 16px;
            font-weight: bold;
            box-sizing: border-box;
            transition: opacity 0.2s;
        }
        .btn-primary {
            background-color: #4CC9F0;
            color: #FFFFFF;
        }
        .btn-secondary {
            background-color: #FFFFFF;
            color: {{ PINK }};
            border: 2px solid {{ PINK }};
        }
        .btn:hover {
            opacity: 0.9;
        }
        .content-box {
            text-align: left;
            margin: 20px 0;
            padding: 15px;
            background: #FAFAFA;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ title }}</h1>
        
        {% if kind == 'menu' %}
            <div class="btn-container">
                {% for label, target in options.items() %}
                    <a href="{{ url_for('navigate', route=target) }}" class="btn {% if is_home and loop.first %}btn-primary{% else %}btn-secondary{% endif %}">{{ label }}</a>
                {% endfor %}
                {% if back %}
                    <a href="{{ url_for('navigate', route=back) }}" class="btn btn-secondary">← Retour</a>
                {% endif %}
            </div>
        {% elif kind == 'content' %}
            <div class="content-box">
                {{ html_content | safe }}
            </div>
            <div class="btn-container">
                <a href="{{ url_for('navigate', route=back) }}" class="btn btn-secondary">← Revenir</a>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return redirect(url_for('navigate', route='home'))

@app.route('/route/<route>')
def navigate(route):
    if route in MENUS:
        data = MENUS[route]
        options_dict = {label: data["routes"][label] for label in data["options"] if label in data["routes"]}
        return render_template_string(
            TEMPLATE,
            title=data["title"],
            kind="menu",
            options=options_dict,
            back=data.get("back"),
            is_home=(route == "home"),
            BG=BG, INK=INK, PINK=PINK, BLUE=BLUE, CYAN=CYAN, GREEN=GREEN
        )
    elif route in CONTENT:
        data = CONTENT[route]
        heading = data.get("title") or route.replace("_", " ").title()
        return render_template_string(
            TEMPLATE,
            title=heading,
            kind="content",
            html_content=data.get("html", "<p>Contenu non disponible</p>"),
            back=data.get("back", "home"),
            BG=BG, INK=INK, PINK=PINK, BLUE=BLUE, CYAN=CYAN, GREEN=GREEN
        )
    else:
        return render_template_string(
            TEMPLATE,
            title="Page non trouvée",
            kind="content",
            html_content="<p style='color:#B91C1C; text-align:center; font-weight:bold;'>Cette page n’a pas été trouvée.</p>",
            back="home",
            BG=BG, INK=INK, PINK=PINK, BLUE=BLUE, CYAN=CYAN, GREEN=GREEN
        )

if __name__ == "__main__":
    app.run()

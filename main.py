
# -*- coding: utf-8 -*-
"""
VerjoResultAccess - Flask Android / PC
Version : Résultat non disponible

Installation :
python -m pip install flask

Lancement :
python VerjoResultAccess_FLASK_ANDROID_PC.py

PC : http://127.0.0.1:5000
Android : http://IP_DU_PC:5000
"""

from pathlib import Path

from flask import Flask, request, render_template_string, send_from_directory

app = Flask(__name__)
app.config["SECRET_KEY"] = "verjo-result-access-local-2026"

BASE_DIR = Path(__file__).resolve().parent


PAGE = r'''<!doctype html>
<html lang="fr">

<head>
    <meta charset="utf-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1, viewport-fit=cover">

    <meta name="theme-color" content="#2563eb">

    <title>Résultat test d'accès en Gestion Ankatso en 2026</title>

    <style>

        :root {
            color-scheme: light;
            --blue: #2563eb;
            --blue2: #1d4ed8;
            --ink: #0f172a;
            --muted: #475569;
        }

        * {
            box-sizing: border-box;
        }

        html {
            min-height: 100%;
            width: 100%;
            overflow-x: hidden;
        }

        body {
            margin: 0;
            padding: clamp(10px, 2.5vw, 22px);
            padding-bottom: max(18px, env(safe-area-inset-bottom));
            width: 100%;
            min-height: 100vh;
            overflow-x: hidden;
            background: #f8fafc;
            color: var(--ink);
            font-family: Arial, Helvetica, sans-serif;
        }

        .page {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
        }

        /* BOUTON AGRANDIR */

        .topbar {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            min-height: 30px;
            margin-bottom: 7px;
        }

        .expand {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 38px;
            min-height: 34px;
            padding: 4px 10px;
            border: 1px solid #cbd5e1;
            border-radius: 7px;
            background: #e2e8f0;
            color: #1e293b;
            font-size: 20px;
            cursor: pointer;
        }

        /* EN-TETE */

        .header {
            display: flex;
            align-items: center;
            gap: 12px;
            width: 100%;
            min-width: 0;
            padding: clamp(12px, 2.5vw, 22px);
            border-radius: 10px;
            background: linear-gradient(
                100deg,
                var(--blue),
                var(--blue2)
            );
            color: white;
        }

        .header h1 {
            flex: 1;
            min-width: 0;
            margin: 0;
            font-size: clamp(17px, 2.4vw, 25px);
            line-height: 1.3;
            overflow-wrap: anywhere;
        }

        .logo {
            width: clamp(48px, 10vw, 100px);
            height: clamp(42px, 8vw, 80px);
            flex: 0 0 auto;
            object-fit: contain;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            background: white;
        }

        /* PRESENTATION */

        .intro {
            margin-top: 14px;
            padding: clamp(12px, 2.5vw, 20px);
            border: 1px solid #cbd5e1;
            border-radius: 9px;
            background: white;
            overflow-wrap: anywhere;
        }

        .session {
            display: inline-block;
            padding: 4px 8px;
            background: #1e293b;
            color: white;
            font-weight: bold;
            font-size: 14px;
        }

        .intro h2 {
            margin: 12px 0 6px;
            font-size: clamp(18px, 2.2vw, 23px);
            line-height: 1.3;
        }

        .intro p {
            margin: 0 0 10px;
            color: var(--muted);
            line-height: 1.5;
        }

        .intro h3 {
            margin: 8px 0 4px;
            font-size: 16px;
        }

        .intro ul {
            margin: 4px 0 0;
            padding-left: 22px;
            line-height: 1.5;
        }

        .intro li strong {
            color: var(--blue);
        }

        /* FORMULAIRE */

        .search-form {
            display: grid;
            grid-template-columns:
                minmax(160px, 1fr)
                minmax(180px, 2fr)
                minmax(180px, 2fr);

            gap: 10px;
            margin-top: 16px;
        }

        .field {
            min-width: 0;
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .field label {
            font-weight: 600;
            font-size: 14px;
            color: #334155;
        }

        input, select {
            width: 100%;
            min-width: 0;
            min-height: 48px;
            padding: 10px 12px;
            border: 1px solid #cbd5e1;
            border-radius: 7px;
            background: white;
            color: #111827;
            font: inherit;
            font-size: 16px;
        }

        input:focus, select:focus {
            outline: 3px solid #bfdbfe;
            border-color: var(--blue);
        }

        .matricule {
            grid-column: 1 / -1;
        }

        .submit {
            grid-column: 1 / -1;
            width: 100%;
            min-height: 52px;
            border: 0;
            border-radius: 7px;
            background: #dc2626;
            color: white;
            font-size: clamp(17px, 2vw, 21px);
            font-weight: bold;
            cursor: pointer;
        }

        .submit:active {
            background: #991b1b;
            transform: translateY(1px);
        }

        /* ZONE CENTRALE : STYLE LISTWIDGET */

        .results {
            margin-top: 18px;
            padding: clamp(12px, 3vw, 24px);

            width: 100%;
            min-height: clamp(250px, 38vh, 380px);

            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;

            border: 2px solid #334155;
            border-radius: 12px;

            background: linear-gradient(
                145deg,
                #f1f5f9,
                #dbeafe
            );

            overflow: hidden;
        }

        /* CARTE DU MESSAGE */

        .unavailable-card {
            width: 100%;
            max-width: 700px;

            margin: auto;
            padding: clamp(20px, 4vw, 36px);

            border: 1px solid #dbeafe;
            border-radius: 18px;

            background: rgba(255, 255, 255, 0.97);

            box-shadow:
                0 12px 30px rgba(30, 64, 175, 0.12);
        }

        .notice-symbol {
            width: 62px;
            height: 62px;

            margin: 0 auto 15px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 50%;

            background: #eff6ff;
            border: 2px solid #bfdbfe;

            color: #2563eb;

            font-family: Georgia, serif;
            font-size: 34px;
            font-weight: bold;
        }

        .notice-kicker {
            margin: 0 0 12px;

            color: #64748b;

            font-size: clamp(11px, 2vw, 13px);
            font-weight: 800;
            letter-spacing: 0.22em;
            text-transform: uppercase;
        }

        /* ECRITURE PRINCIPALE */

        .notice-title {
            margin: 0;

            color: #172554;

            font-family: Georgia, "Times New Roman", serif;

            font-size: clamp(25px, 5vw, 43px);

            font-weight: 700;
            line-height: 1.2;

            letter-spacing: 0.01em;

            overflow-wrap: anywhere;
        }

        .notice-title span {
            display: block;

            color: #2563eb;

            font-style: italic;
        }

        .notice-line {
            width: 80px;
            height: 4px;

            margin: 20px auto;

            border-radius: 10px;

            background: linear-gradient(
                90deg,
                #93c5fd,
                #2563eb
            );
        }

        .notice-message {
            max-width: 530px;

            margin: 0 auto;

            color: #475569;

            font-size: clamp(14px, 2.2vw, 17px);
            line-height: 1.7;

            overflow-wrap: anywhere;
        }

        .notice-foot {
            margin: 20px 0 0;

            color: #94a3b8;

            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.12em;

            text-transform: uppercase;
        }

        /* RESPONSIVE ANDROID */

        @media (max-width: 650px) {

            body {
                padding: 10px;
                padding-bottom: max(
                    16px,
                    env(safe-area-inset-bottom)
                );
            }

            .header {
                gap: 8px;
                padding: 12px;
            }

            .header h1 {
                font-size: clamp(16px, 4.5vw, 20px);
            }

            .search-form {
                grid-template-columns: minmax(0, 1fr);
                gap: 9px;
            }

            .field,
            .matricule,
            .submit {
                grid-column: 1;
            }

            .field label {
                font-size: 14px;
            }

            input, select {
                min-height: 50px;
                font-size: 16px;
            }

            .intro {
                margin-top: 10px;
                padding: 13px;
            }

            .intro h2 {
                font-size: 19px;
            }

            .results {
                margin-top: 12px;
                padding: 10px;
                min-height: 260px;
            }

            .unavailable-card {
                padding: 20px 14px;
            }

            .notice-symbol {
                width: 50px;
                height: 50px;
                font-size: 27px;
                margin-bottom: 12px;
            }

            .notice-line {
                margin: 15px auto;
            }
        }

        @media (min-width: 651px) and (max-width: 850px) {

            .search-form {
                grid-template-columns:
                    minmax(0, 1fr)
                    minmax(0, 2fr);
            }

            .field:nth-child(3) {
                grid-column: 1 / -1;
            }
        }

    </style>

    <script>

        function toggleFullscreen() {

            if (!document.fullscreenElement) {

                document.documentElement
                    .requestFullscreen?.()
                    .catch(() => {});

            } else {

                document.exitFullscreen?.();

            }
        }

    </script>

</head>

<body>

<div class="page">

    <!-- AGRANDISSEMENT PC -->

    <div class="topbar">

        <button
            class="expand"
            type="button"
            onclick="toggleFullscreen()"
            aria-label="Agrandir ou restaurer"
            title="Agrandir / restaurer">

            ⛶

        </button>

    </div>


    <!-- EN-TETE -->

    <header class="header">

        <h1>
            Résultat test d'accès en Gestion Ankatso en 2026
        </h1>

        {% if logo_exists %}

        <img
            class="logo"
            src="{{ url_for('logo') }}"
            alt="Logo Gestion">

        {% endif %}

    </header>


    <!-- PRESENTATION -->

    <section class="intro">

        <span class="session">
            SESSION 2026
        </span>

        <h2>
            Test d'Accès en 1ère Année — Gestion
        </h2>

        <p>
            L'épreuve d'accès en première année de gestion
            vise à évaluer les acquis fondamentaux et les
            capacités d'analyse des candidats à travers
            deux épreuves d'évaluation.
        </p>

        <h3>
            Matières évaluées :
        </h3>

        <ul>

            <li>
                <strong>Culture Générale :</strong>
                Évaluation de la réflexion globale,
                de la logique et de l'ouverture sur le monde.
            </li>

            <li>
                <strong>Connaissances sur l'Entreprise :</strong>
                Évaluation des notions de base sur le
                fonctionnement et le monde des affaires.
            </li>

        </ul>

    </section>


    <!-- FORMULAIRE CONSERVE -->

    <form
        class="search-form"
        method="post"
        action="{{ url_for('index') }}">

        <div class="field">

            <label for="centre">
                Centre
            </label>

            <select id="centre" name="centre">

                <option
                    value="Sélectionner le centre"
                    {% if centre == 'Sélectionner le centre' %}
                    selected
                    {% endif %}>

                    Sélectionner le centre

                </option>

                <option
                    value="Ankatso"
                    {% if centre == 'Ankatso' %}
                    selected
                    {% endif %}>

                    Ankatso

                </option>

            </select>

        </div>


        <div class="field">

            <label for="nom">
                Nom (mot-clé)
            </label>

            <input
                id="nom"
                name="nom"
                type="search"
                placeholder="Votre nom (ou mot-clé)"
                value="{{ nom }}"
                autocomplete="off">

        </div>


        <div class="field">

            <label for="prenom">
                Prénom (mot-clé)
            </label>

            <input
                id="prenom"
                name="prenom"
                type="search"
                placeholder="Votre prénom (ou mot-clé)"
                value="{{ prenom }}"
                autocomplete="off">

        </div>


        <div class="field matricule">

            <label for="matricule">
                Numéro matricule
            </label>

            <input
                id="matricule"
                name="matricule"
                type="search"
                placeholder="Ex : 278.g.tnr.30 (optionnel)"
                value="{{ matricule }}"
                autocomplete="off">

        </div>


        <button class="submit" type="submit">

            Valider la recherche

        </button>

    </form>


    <!-- PANNEAU CENTRAL TYPE QLISTWIDGET -->

    <section
        class="results"
        aria-live="polite"
        aria-label="Disponibilité des résultats">

        <div class="unavailable-card" role="status">

            <div class="notice-symbol" aria-hidden="true">
                i
            </div>

            <p class="notice-kicker">

                INFORMATION OFFICIELLE

            </p>

            <h2 class="notice-title">

                Résultat

                <span>
                    non disponible
                </span>

            </h2>

            <div class="notice-line"></div>

            <p class="notice-message">

                Les résultats ne sont pas encore disponibles
                à la consultation.

                Merci de revenir ultérieurement pour obtenir
                les informations mises à jour.

            </p>

            <p class="notice-foot">

                SESSION 2026 · GESTION · ANKATSO

            </p>

        </div>

    </section>


</div>

</body>
</html>
'''


# ROUTE DU LOGO
@app.route("/logo")
def logo():

    return send_from_directory(
        str(BASE_DIR),
        "gestion.jpg"
    )


# PAGE PRINCIPALE
@app.route("/", methods=["GET", "POST"])
def index():

    # Conservation des champs du formulaire.
    # Aucune donnée d'étudiant n'est chargée.

    centre = request.form.get(
        "centre",
        "Sélectionner le centre"
    ).strip()

    nom = request.form.get(
        "nom",
        ""
    ).strip()

    prenom = request.form.get(
        "prenom",
        ""
    ).strip()

    matricule = request.form.get(
        "matricule",
        ""
    ).strip()

    return render_template_string(

        PAGE,

        logo_exists=(
            BASE_DIR / "gestion.jpg"
        ).is_file(),

        centre=centre,
        nom=nom,
        prenom=prenom,
        matricule=matricule

    )


# DEMARRAGE DU SERVEUR
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )

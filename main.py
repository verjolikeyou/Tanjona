# -*- coding: utf-8 -*-
"""VerjoResultAccess - version Flask responsive Android / PC.

Installation : python -m pip install flask
Lancement    : python VerjoResultAccess_FLASK_ANDROID_PC.py
Ouverture PC : http://127.0.0.1:5000
Ouverture Android (même Wi-Fi que le PC) : http://IP_DU_PC:5000
"""

from flask import Flask, request, render_template_string, send_from_directory
from markupsafe import escape
from pathlib import Path

app = Flask(__name__)
app.config["SECRET_KEY"] = "verjo-result-access-local-2026"
BASE_DIR = Path(__file__).resolve().parent

# Base de données complète : les 15 étudiants de la version PySide6.
LISTE_ETUDIANTS = [
    {"id": 1, "nom": "raobijhon", "prenom": "miharintsoa toby", "matricule": "278.g.tnr.30", "affichage": "Raobijhon Miharintsoa Toky", "statut": "admis"},
    {"id": 2, "nom": "abolatiana", "prenom": "rahaja", "matricule": "278.g.tnr.31", "affichage": "Abolatiana Rahaja", "statut": "admis"},
    {"id": 3, "nom": "nono", "prenom": "tiderana", "matricule": "278.g.tnr.32", "affichage": "Nono Tiderana", "statut": "admis"},
    {"id": 4, "nom": "manono", "prenom": "menja", "matricule": "278.g.tnr.33", "affichage": "Manono Menja", "statut": "admis"},
    {"id": 5, "nom": "rika", "prenom": "razafimahaleo", "matricule": "278.g.tnr.34", "affichage": "Rika Razafimahaleo", "statut": "admis"},
    {"id": 6, "nom": "mino", "prenom": "razafimamantsoa", "matricule": "278.g.tnr.35", "affichage": "Mino Razafimamantsoa", "statut": "admis"},
    {"id": 7, "nom": "randriamirina", "prenom": "tiderana", "matricule": "278.g.tnr.36", "affichage": "Randriamirina Tiderana", "statut": "admis"},
    {"id": 8, "nom": "henintsoa", "prenom": "gael", "matricule": "278.g.tnr.37", "affichage": "Henintsoa Gael", "statut": "admis"},
    {"id": 9, "nom": "raminja", "prenom": "vololonirina", "matricule": "278.g.tnr.38", "affichage": "Raminja Vololonirina", "statut": "admis"},
    {"id": 10, "nom": "robjhon", "prenom": "tanjoniaina rivo", "matricule": "278.g.tnr.27", "affichage": "Robjhon Tanjoniaina Rivo", "statut": "admis"},
    {"id": 11, "nom": "andrianina", "prenom": "luc", "matricule": "278.g.tnr.39", "affichage": "Andrianina Luc", "statut": "admis"},
    {"id": 12, "nom": "soa", "prenom": "hasina", "matricule": "278.g.tnr.40", "affichage": "Soa Hasina", "statut": "admis"},
    {"id": 13, "nom": "fetra", "prenom": "ny aina", "matricule": "278.g.tnr.41", "affichage": "Fetra Ny Aina", "statut": "admis"},
    {"id": 14, "nom": "boto", "prenom": "kely", "matricule": "278.g.tnr.42", "affichage": "Boto Kely", "statut": "non_admis"},
    {"id": 15, "nom": "be", "prenom": "lahy", "matricule": "278.g.tnr.43", "affichage": "Be Lahy", "statut": "non_admis"},
]

PAGE = r'''<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#2563eb">
  <title>Résultat test d'accès en Gestion Ankatso en 2026</title>
  <style>
    :root { color-scheme: light; --blue:#2563eb; --blue2:#1d4ed8; --ink:#0f172a; --muted:#475569; }
    * { box-sizing:border-box; }
    html { min-height:100%; width:100%; overflow-x:hidden; }
    body { margin:0; padding:clamp(10px,2.5vw,22px); padding-bottom:max(18px,env(safe-area-inset-bottom));
           width:100%; min-height:100vh; overflow-x:hidden; background:#f8fafc;
           color:var(--ink); font-family:Arial,Helvetica,sans-serif; }
    .page { width:100%; max-width:1200px; margin:0 auto; }
    .topbar { display:flex; justify-content:flex-end; align-items:center; min-height:25px; margin-bottom:7px; }
    .expand { display:inline-flex; align-items:center; justify-content:center; min-width:30px; min-height:28px;
              padding:3px 8px; border:1px solid #cbd5e1; border-radius:6px; background:#e2e8f0;
              color:#1e293b; font-size:17px; text-decoration:none; cursor:pointer; }
    .header { display:flex; align-items:center; gap:12px; width:100%; min-width:0;
              padding:clamp(12px,2.5vw,22px); border-radius:10px;
              background:linear-gradient(100deg,var(--blue),var(--blue2)); color:white; }
    .header h1 { flex:1; min-width:0; margin:0; font-size:clamp(17px,2.4vw,25px); line-height:1.3; overflow-wrap:anywhere; }
    .logo { width:clamp(48px,10vw,100px); height:clamp(42px,8vw,80px); flex:0 0 auto; object-fit:contain;
            border:1px solid #cbd5e1; border-radius:6px; background:#fff; }
    .intro { margin-top:14px; padding:clamp(12px,2.5vw,20px); border:1px solid #cbd5e1;
             border-radius:9px; background:white; overflow-wrap:anywhere; }
    .session { display:inline-block; padding:2px 6px; background:#1e293b; color:white; font-weight:bold; font-size:14px; }
    .intro h2 { margin:12px 0 6px; font-size:clamp(18px,2.2vw,23px); line-height:1.3; }
    .intro p { margin:0 0 10px; color:var(--muted); line-height:1.5; }
    .intro h3 { margin:8px 0 4px; font-size:16px; }
    .intro ul { margin:4px 0 0; padding-left:22px; line-height:1.5; }
    .intro li strong { color:var(--blue); }
    .search-form { display:grid; grid-template-columns:minmax(160px,1fr) minmax(180px,2fr) minmax(180px,2fr);
                   gap:10px; margin-top:16px; }
    .field { min-width:0; display:flex; flex-direction:column; gap:5px; }
    .field label { font-weight:600; font-size:14px; color:#334155; }
    input, select { width:100%; min-width:0; min-height:48px; padding:10px 12px; border:1px solid #cbd5e1;
                    border-radius:7px; background:white; color:#111827; font:inherit; font-size:16px; }
    input:focus, select:focus { outline:3px solid #bfdbfe; border-color:var(--blue); }
    .matricule { grid-column:1 / -1; }
    .submit { grid-column:1 / -1; width:100%; min-height:52px; border:0; border-radius:7px;
              background:#dc2626; color:white; font-size:clamp(17px,2vw,21px); font-weight:bold; cursor:pointer; }
    .submit:active { background:#991b1b; transform:translateY(1px); }
    .results { margin-top:16px; padding:8px; border:2px solid #334155; border-radius:9px;
               background:#f8fafc; min-height:180px; }
    .result { display:block; width:100%; margin:0 0 2px; padding:8px 9px; border-radius:3px;
              font-size:clamp(14px,1.4vw,17px); line-height:1.45; font-weight:700;
              overflow-wrap:anywhere; word-break:normal; }
    .admis { background:#dcfce7; color:#166534; }
    .non-admis { background:#fee2e2; color:#991b1b; }
    .warning { background:#fef3c7; color:#92400e; }
    .empty { background:#fee2e2; color:#991b1b; }
    .details { display:block; font-weight:600; }
    .count { margin:8px 2px 2px; color:#475569; font-size:13px; }
    @media (max-width:650px) {
      body { padding:10px; padding-bottom:max(16px,env(safe-area-inset-bottom)); }
      .header { gap:8px; padding:12px; }
      .header h1 { font-size:clamp(16px,4.5vw,20px); }
      .search-form { grid-template-columns:minmax(0,1fr); gap:9px; }
      .field, .matricule, .submit { grid-column:1; }
      .field label { font-size:14px; }
      input, select { min-height:50px; font-size:16px; }
      .intro { margin-top:10px; padding:13px; }
      .intro h2 { font-size:19px; }
      .results { margin-top:12px; padding:5px; min-height:220px; }
      .result { padding:8px; font-size:14px; line-height:1.5; }
    }
    @media (min-width:651px) and (max-width:850px) {
      .search-form { grid-template-columns:minmax(0,1fr) minmax(0,2fr); }
      .field:nth-child(3) { grid-column:1 / -1; }
    }
  </style>
  <script>
    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen?.().catch(() => {});
      } else {
        document.exitFullscreen?.();
      }
    }
  </script>
</head>
<body>
<div class="page">
  <div class="topbar"><button class="expand" type="button" onclick="toggleFullscreen()" aria-label="Agrandir ou restaurer" title="Agrandir / restaurer">⛶</button></div>
  <header class="header">
    <h1>Résultat test d'accès en Gestion Ankatso en 2026</h1>
    {% if logo_exists %}<img class="logo" src="{{ url_for('logo') }}" alt="Logo Gestion">{% endif %}
  </header>

  <section class="intro">
    <span class="session">SESSION 2026</span>
    <h2>Test d'Accès en 1ère Année — Gestion</h2>
    <p>L'épreuve d'accès en première année de gestion vise à évaluer les acquis fondamentaux et les capacités d'analyse des candidats à travers deux épreuves d'évaluation.</p>
    <h3>Matières évaluées :</h3>
    <ul>
      <li><strong>Culture Générale :</strong> Évaluation de la réflexion globale, de la logique et de l'ouverture sur le monde.</li>
      <li><strong>Connaissances sur l'Entreprise :</strong> Évaluation des notions de base sur le fonctionnement et le monde des affaires.</li>
    </ul>
  </section>

  <form class="search-form" method="post" action="{{ url_for('index') }}">
    <div class="field">
      <label for="centre">Centre</label>
      <select id="centre" name="centre">
        <option value="Sélectionner le centre" {% if centre == 'Sélectionner le centre' %}selected{% endif %}>Sélectionner le centre</option>
        <option value="Ankatso" {% if centre == 'Ankatso' %}selected{% endif %}>Ankatso</option>
      </select>
    </div>
    <div class="field">
      <label for="nom">Nom (mot-clé)</label>
      <input id="nom" name="nom" type="search" placeholder="Votre nom (ou mot-clé)" value="{{ nom }}" autocomplete="off">
    </div>
    <div class="field">
      <label for="prenom">Prénom (mot-clé)</label>
      <input id="prenom" name="prenom" type="search" placeholder="Votre prénom (ou mot-clé)" value="{{ prenom }}" autocomplete="off">
    </div>
    <div class="field matricule">
      <label for="matricule">Numéro matricule</label>
      <input id="matricule" name="matricule" type="search" placeholder="Ex : 278.g.tnr.30 (optionnel)" value="{{ matricule }}" autocomplete="off">
    </div>
    <button class="submit" type="submit">Valider la recherche</button>
  </form>

  <section class="results" aria-live="polite" aria-label="Résultats de recherche">
    {% for etu in resultats %}
      <article class="result {{ 'admis' if etu.statut == 'admis' else 'non-admis' }}">
        {{ etu.id }}. {{ '✅ ADMIS' if etu.statut == 'admis' else '❌ NON ADMIS' }} — {{ etu.affichage }}
        <span class="details">Matricule : {{ etu.matricule }} | Centre : Ankatso</span>
      </article>
    {% endfor %}
    {% if message %}<article class="result {{ message_class }}">{{ message }}</article>{% endif %}
    {% if searched and not message %}<p class="count">{{ resultats|length }} résultat(s) trouvé(s).</p>{% endif %}
  </section>
</div>
</body>
</html>'''


@app.route("/logo")
def logo():
    # Le fichier gestion.jpg reste facultatif et doit être placé à côté du .py.
    return send_from_directory(str(BASE_DIR), "gestion.jpg")


@app.route("/", methods=["GET", "POST"])
def index():
    centre = request.form.get("centre", "Sélectionner le centre").strip()
    nom = request.form.get("nom", "").strip()
    prenom = request.form.get("prenom", "").strip()
    matricule = request.form.get("matricule", "").strip()
    resultats = LISTE_ETUDIANTS[:]
    message = ""
    message_class = ""
    searched = request.method == "POST"

    if searched:
        nom_c = nom.casefold()
        prenom_c = prenom.casefold()
        matricule_c = matricule.casefold()

        if not nom_c and not prenom_c and not matricule_c:
            resultats = []
            message = "Veuillez remplir au moins un champ (Nom, Prénom ou Matricule) pour lancer la recherche."
            message_class = "warning"
        elif centre != "Ankatso":
            resultats = []
            message = f"⚠️ Erreur de Centre : « {centre} » n'est pas autorisé. Seul le centre Ankatso est accepté."
            message_class = "warning"
        else:
            # Même règle que la version PySide6 : les critères remplis sont
            # combinés par OU et chaque recherche accepte une correspondance partielle.
            resultats = []
            for etu in LISTE_ETUDIANTS:
                correspond_nom = bool(nom_c) and (nom_c in etu["nom"].casefold() or nom_c in etu["prenom"].casefold())
                correspond_prenom = bool(prenom_c) and (prenom_c in etu["nom"].casefold() or prenom_c in etu["prenom"].casefold())
                correspond_matricule = bool(matricule_c) and matricule_c in etu["matricule"].casefold()
                if correspond_nom or correspond_prenom or correspond_matricule:
                    resultats.append(etu)
            if not resultats:
                message = ("❌ Aucun résultat trouvé pour votre recherche "
                           f"(Nom : « {nom} », Prénom : « {prenom} », Matricule : « {matricule} »).")
                message_class = "empty"

    return render_template_string(
        PAGE,
        resultats=resultats,
        message=message,
        message_class=message_class,
        searched=searched,
        centre=centre,
        nom=nom,
        prenom=prenom,
        matricule=matricule,
        logo_exists=(BASE_DIR / "gestion.jpg").is_file(),
    )


if __name__ == "__main__":
    # Accessible sur le PC et sur les autres appareils du même réseau Wi-Fi.
    # En production publique, utiliser un serveur WSGI et activer HTTPS.
    app.run(host="0.0.0.0", port=5000, debug=False)

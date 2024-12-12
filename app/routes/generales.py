from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "random_secret_key"  # Changez pour production

# Configuration OAuth avec Keycloak
oauth = OAuth(app)

# Base de données temporaire (simulation)
users = {}

# Route pour l'accueil
@app.route("/")
def home():
    return render_template("home.html")

# Route pour le login avec ORCID
@app.route("/login")
def login():
    redirect_uri = url_for("authorize", _external=True)
    return oauth.keycloak.authorize_redirect(redirect_uri)

# Route de callback après l'authentification
@app.route("/authorize")
def authorize():
    token = oauth.keycloak.authorize_access_token()
    user_info = token.get('userinfo')
    session['user'] = user_info

    # Gestion des utilisateurs
    email = user_info['email']
    if email not in users:
        # Nouvel utilisateur -> page d'inscription
        return redirect(url_for("register"))
    return redirect(url_for("dashboard"))

# Route pour l'inscription
@app.route("/register", methods=["GET", "POST"])
def register():
    if "user" not in session:
        return redirect(url_for("login"))
    user_info = session["user"]
    users[user_info["email"]] = user_info  # Enregistrer l'utilisateur
    return redirect(url_for("dashboard"))

# Route pour le tableau de bord
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

# Route pour se déconnecter
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

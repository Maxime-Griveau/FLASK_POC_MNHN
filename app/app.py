import os
from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "1515151555"  # Changez pour production

# Configuration OAuth avec Keycloak
oauth = OAuth(app)
oauth.register(
    name='keycloak',
    client_id='flask-client',  # ID du client Keycloak
    client_secret='GUWM9YghDu9VaP91SJBTI9caQIaCJ94R',  # Secret Keycloak
    server_metadata_url='https://keycloak-production-8f36.up.railway.app/realms/myrealm/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# Base de données temporaire (simulation)
users = {}

# Route pour l'accueil
@app.route("/")
def home():
    return render_template("home.html")

# Route pour le login avec ORCID
@app.route("/login")
def login():
    redirect_uri = "https://keycloak-production-8f36.up.railway.app/realms/myrealm/.well-known/openid-configuration"
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

if __name__ == "__main__":
    # Assurez-vous de lire le port depuis l'environnement
    port = int(os.environ.get("PORT", 5000))
    # Utilisez host="0.0.0.0" pour écouter sur toutes les interfaces réseau
    app.run(host="0.0.0.0", port=port)
import os
from app import app  # Importez votre application Flask depuis `app.py`

if __name__ == "__main__":
    # Récupérer le port depuis les variables d'environnement
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

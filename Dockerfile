# Utiliser une image légère pour Python
FROM python:3.10-slim


# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier uniquement requirements.txt d'abord (meilleur cache Docker)
COPY requirements.txt .

# Mettre à jour pip et installer les dépendances
# Mettre à jour et installer curl
RUN apt-get update && apt-get install -y curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


# Configurer Flask pour qu'il sache où se trouve l'application
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=True


# Copier tout le contenu du projet dans le conteneur
COPY . .


# Exposer le port 5000 (par défaut pour Flask)
EXPOSE 5000

# Lancer l'application Flask
CMD ["flask", "run", "--host=0.0.0.0"]



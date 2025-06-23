FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers dans le conteneur
COPY . .

# Créer le dossier de logs et attribuer les bonnes permissions
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Démarrer l'application
CMD ["python", "app.py"]

# Utiliser une image de base légère pour Python
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port que l'application utilise (par exemple, 8000 pour FastAPI)
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


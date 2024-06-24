# Utiliser une image de base pour le frontend (par exemple, Node.js pour une application React)
FROM node:20

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste des fichiers de l'application
COPY . .

# Exposer le port que l'application utilise (par exemple, 3000 pour React)
EXPOSE 3000

# Commande pour démarrer l'application
CMD ["npm", "start"]





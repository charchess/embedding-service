# Utilise une image Python légère comme base
FROM python:3.11-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie le fichier des dépendances
COPY requirements.txt .

# Installe les dépendances
# --no-cache-dir réduit la taille de l'image finale
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code de notre service dans le conteneur
COPY embedding_service.py .

# Expose le port que notre service va utiliser
EXPOSE 8001

# La commande pour lancer le service quand le conteneur démarre
# Uvicorn est le serveur qui fait tourner notre application FastAPI
# --host 0.0.0.0 est essentiel pour que le service soit accessible depuis l'extérieur du conteneur
CMD ["uvicorn", "embedding_service:app", "--host", "0.0.0.0", "--port", "8001"]

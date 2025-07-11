from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import torch

# Détermine si un GPU est disponible pour l'utiliser si possible, sinon utilise le CPU
# Pour votre swarm "vixen", ce sera très probablement 'cpu'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Embedding service is using device: {device}")

# Charge le modèle d'embedding UNE SEULE FOIS au démarrage du service.
# C'est crucial pour les performances.
# 'all-MiniLM-L6-v2' est un excellent choix, petit et performant.
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
print("Embedding model loaded successfully.")

# Initialise l'application FastAPI
app = FastAPI()

# Définit la structure des données que notre API attend en entrée (du texte)
class TextInput(BaseModel):
    text: str

# Définit le point d'accès (endpoint) de notre API
@app.post("/embed")
async def create_embedding(data: TextInput):
    # Utilise le modèle chargé pour convertir le texte en vecteur
    embedding = model.encode(data.text).tolist()

    # Renvoie le vecteur sous forme de réponse JSON
    return {"text": data.text, "embedding": embedding}

# Un petit endpoint pour vérifier que le service est en vie
@app.get("/health")
async def health_check():
    return {"status": "ok"}
    
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from src.mydatabase import engine
from src import models
from src.routers import compteur
from src.routers import recharge
from src.routers import typeCompteur

models.Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True, 
              title="Sunu Woyafal", 
              description="Avec Woyofal, l’électricité prépayée, soyez enfin tranquille !"
            )
app.include_router(compteur.router_compteur)
app.include_router(recharge.router_recharge)
app.include_router(typeCompteur.router_typeCompteur)

origins = ["http://localhost:3000","http://127.0.0.1:3000","http://localhost:3030","http://127.0.0.1:3030"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CompteurStatus(BaseModel):
    statusCompteur: Optional[bool] = True


class CompteurType(BaseModel):
    immatricule: str


class CompteurNumero(BaseModel):
    numeroCompteur: int

class CompteurKwDispo(BaseModel):
    totalKwDispo: float = 0.0


class CompteurCreditUrgence(BaseModel):
    creditUrgence: bool = False


class CompteurBase(CompteurNumero, CompteurType):
    prenom: str = None
    nom: str = None
    adresse: str = None


class CompteurNew(CompteurBase):
    pass

class Compteur(CompteurBase):
    dateAcquisition: Optional[datetime] = datetime.now()


class CompteurRechargeUpdate(CompteurNumero, CompteurKwDispo):
    pass


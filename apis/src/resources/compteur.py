from ..schemas.compteur import CompteurNew, CompteurStatus, Compteur, CompteurType
from sqlalchemy.orm import Session
from datetime import datetime
from ..config.variable import LEN_DIGIT_COMPTEUR
from .. import models


def new_compteur(db: Session, compteur:CompteurNew):
    db_compteur = models.Compteur(**compteur.model_dump())
    db_compteur.dateAcquisition = datetime.now()
    db.add(db_compteur)
    db.commit()
    return db_compteur


def get_compteur(db:Session, numeroCompteur: int):
    return db.query(models.Compteur).filter(models.Compteur.numeroCompteur == numeroCompteur).first()
    

def check_len_compteur(numeroCompteur):
    return len(str(numeroCompteur)) == LEN_DIGIT_COMPTEUR


def update_compteur_status(db:Session, db_compteur:Compteur, compteur_status_update:CompteurStatus):
    db_compteur.statusCompteur = compteur_status_update.statusCompteur
    db.commit()
    db.refresh(db_compteur)
    return db_compteur


def update_compteur_type(db:Session, db_compteur:Compteur, compteur_type_update:CompteurType):
    db_compteur.typeCompteur = compteur_type_update.typeCompteur
    db.commit()
    db.refresh(db_compteur)
    return db_compteur


def get_total_kw_dispo(db:Session, numeroCompteur:int):
    return db.query(models.Compteur).filter(models.Compteur.numeroCompteur == numeroCompteur).first()


def update_total_kw_dispo(db:Session, compteur: Compteur, new_kw: float):
    compteur.totalKwDispo += new_kw
    print(dir(compteur))
    db.commit()
    db.refresh(compteur)
    return compteur
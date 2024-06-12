from ..schemas.typeCompteur import  TypeCompteurNew
from sqlalchemy.orm import Session
from .. import models

def get_type_compteur(db:Session, immatricule: str):
    return db.query(models.TypeCompteur).filter(models.TypeCompteur.immatricule == immatricule).first()


def new_type_compteur(db: Session, typeCompteur:TypeCompteurNew):
    db_compteur = models.TypeCompteur(**typeCompteur.model_dump())
    db.add(db_compteur)
    db.commit()
    return db_compteur
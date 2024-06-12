from ..schemas.typeCompteur import TypeCompteur, TypeCompteurNew
from fastapi import Depends, APIRouter, HTTPException, status
from ..resources import typeCompteur as resource_typeCompteur
from sqlalchemy.orm import Session
from ..config.mydb import get_db

router_typeCompteur = APIRouter(prefix='/typecompteur', tags=['Type de compteur'])

@router_typeCompteur.get('/get/typecompteur/{immatricule}', response_model=TypeCompteur)
def get_type_compteur(immatricule: str, db:Session = Depends(get_db)):
    db_typecompteur = resource_typeCompteur.get_type_compteur(db=db, immatricule=immatricule)
    if db_typecompteur:
        return db_typecompteur
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='compteur type not found')


@router_typeCompteur.post('/add', response_model=TypeCompteurNew)
def add_new_type_compteur(typeCompteur: TypeCompteurNew, db:Session = Depends(get_db)):
    db_typecompteur = resource_typeCompteur.get_type_compteur(db=db, immatricule=typeCompteur.immatricule)
    if  db_typecompteur:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f'Immatricule exist deja')
    return resource_typeCompteur.new_type_compteur(db=db, typeCompteur=typeCompteur)
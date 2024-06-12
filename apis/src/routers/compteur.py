from ..schemas.compteur import Compteur, CompteurNew, CompteurStatus, CompteurType, CompteurKwDispo, CompteurRechargeUpdate
from fastapi import Depends, APIRouter, HTTPException, status
from ..resources import compteur as resource_compteur
from ..resources.typeCompteur import get_type_compteur
from sqlalchemy.orm import Session
from ..config.mydb import get_db
from ..config.variable import LEN_DIGIT_COMPTEUR


router_compteur = APIRouter(prefix='/compteurs', tags=['Compteurs'])

@router_compteur.post('/addcompteur', response_model=Compteur)
def add_compteur( compteur: CompteurNew, db:Session = Depends(get_db)):
    if not get_type_compteur(db=db, immatricule=compteur.immatricule):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='type compteur not found')
    
    if not resource_compteur.check_len_compteur(compteur.numeroCompteur):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                            detail=f'Compteur doit avoir {LEN_DIGIT_COMPTEUR} chiffres')
    
    db_numeroCompteur = resource_compteur.get_compteur(db=db, numeroCompteur=compteur.numeroCompteur)
    if db_numeroCompteur:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f'Compteur {compteur.numeroCompteur} exist deja')
    
    return resource_compteur.new_compteur(db=db, compteur=compteur)


@router_compteur.get('/getcompteur/{numeroCompteur}', response_model=Compteur)
def get_compteur(numeroCompteur:int, db:Session = Depends(get_db)):
    db_compteur = resource_compteur.get_compteur(db=db, numeroCompteur=numeroCompteur)
    if db_compteur:
        return db_compteur
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Compteur not found')


@router_compteur.get('/get/creditdispo/{numeroCompteur}', response_model=CompteurKwDispo)
def get_total_kw_dispo(numeroCompteur: int, db:Session = Depends(get_db)):
    db_compteur = resource_compteur.get_total_kw_dispo(db=db, numeroCompteur=numeroCompteur)
    if db_compteur:
        return db_compteur
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Compteur not found')


@router_compteur.put('/updatecompteur/status/{numeroCompteur}', response_model=Compteur)
def update_status_compteur(numeroCompteur:int, compteur_update:CompteurStatus, db:Session = Depends(get_db)):
    db_compteur = resource_compteur.get_compteur(db=db, numeroCompteur=numeroCompteur)
    if db_compteur:
        return resource_compteur.update_compteur_status(
            db_compteur=db_compteur,
            compteur_status_update=compteur_update,
            db=db
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Compteur not found')


@router_compteur.put('/updatecompteur/type/{numeroCompteur}', response_model=Compteur)
def update_type_compteur(numeroCompteur:int, compteur_update:CompteurType, db:Session = Depends(get_db)):
    db_compteur = resource_compteur.get_compteur(db=db, numeroCompteur=numeroCompteur)
    
    if db_compteur:
        return resource_compteur.update_compteur_type(
            db_compteur=db_compteur,
            compteur_type_update=compteur_update,
            db=db
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Compteur not found')


@router_compteur.put('/update/creditdispo/{numeroCompteur}', response_model=CompteurRechargeUpdate)
def update_kw_dispo(numeroCompteur: int, compteur_update: CompteurKwDispo, db:Session = Depends(get_db)):
    db_compteur = resource_compteur.get_compteur(db=db, numeroCompteur=numeroCompteur)

    if db_compteur:
        return resource_compteur.update_total_kw_dispo(db=db, compteur=db_compteur,new_kw=compteur_update.totalKwDispo)
    
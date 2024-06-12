from fastapi import Depends, APIRouter, HTTPException, status
from ..schemas.recharge import Recharge, RechargeNew, RechargeQuantite, RechargeCode, RechargeUpdateResponse
from ..resources import recharge as resource_recharge
from ..resources.compteur import get_compteur
from sqlalchemy.orm import Session
from ..config.mydb import get_db
from ..config.variable import MIN_MONTANT_RECHARGE


router_recharge = APIRouter(prefix='/recharge', tags=['Recharge'])


@router_recharge.get('/getrecharge/{idRecharge}', response_model=Recharge)
def get_recharge(idRecharge:int, db:Session = Depends(get_db)):
    db_recharge = resource_recharge.get_recharge(db=db, idRecharge=idRecharge)
    if db_recharge:
        return db_recharge
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Recharge not exist')


@router_recharge.get('/get/currentmonth/{numeroCompteur}', response_model=RechargeQuantite)
def get_recharge_sum_current_month(numeroCompteur: int, db:Session=Depends(get_db)):
    
    db_compteur = get_compteur(db=db, numeroCompteur=numeroCompteur)
    if not db_compteur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Compteur not found')
    
    db_recharge = resource_recharge.get_sum_recharge_current_month(db=db, numeroCompteur=numeroCompteur)
    if db_recharge:
        return db_recharge


@router_recharge.post('/addrecharge', response_model=Recharge)
def add_new_recharge(recharge: RechargeNew, db:Session = Depends(get_db)):
    db_compteur = get_compteur(db=db, numeroCompteur=recharge.numeroCompteur)
    if recharge.montantRecharge < MIN_MONTANT_RECHARGE:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                            detail=f'Min recharge {MIN_MONTANT_RECHARGE} Fcfa')
    if db_compteur:
        return resource_recharge.add_recharge(db=db, recharge=recharge)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='compteur not found')


@router_recharge.put('/update/coderecharge/{numeroCompteur}', response_model=RechargeUpdateResponse)
def submit_code_recharge(numeroCompteur:int, code_recharge:RechargeCode, db:Session = Depends(get_db)):
    db_recharge = resource_recharge.get_recharge_with_code(db=db, 
                                                           numeroCompteur=numeroCompteur,
                                                           codeRecharge=code_recharge.codeRecharge)
    if db_recharge:
        print(f'recharge dir {dir(db_recharge)}')
        if resource_recharge.update_recharge_status(db=db, db_recharge=db_recharge):
            return db_recharge
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail='code deja utilisé')
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='invalid code')
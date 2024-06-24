from ..schemas.recharge import RechargeNew, RechargeQuantiteResponse, RechargeDate, RechargeUpdateResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from .. import models
import secrets
from datetime import datetime
from ..config import variable
from . import compteur




def generate_code_recharge(len_code=variable.LEN_CODE):
    code = ''.join(str(secrets.randbelow(10)) for _ in range(len_code))
    return code


def get_sum_recharge_current_month(db:Session, numeroCompteur: int):
    req = text(""" SELECT ROUND(COALESCE(SUM(quantiteRecharge), 0), 1) as quantiteRecharge 
                    FROM Recharge 
                    WHERE numeroCompteur=:numeroCompteur 
                        AND YEAR(dateRecharge) = YEAR(CURRENT_DATE()) 
                        AND MONTH(dateRecharge) = MONTH(CURRENT_DATE())
            """)
    result = db.execute(req, {'numeroCompteur': numeroCompteur})
    rows = result.fetchall()
    data = []
    cols = result.keys()
    for row in rows:
        data.append(dict(zip(cols, row)))
    return  data[0]


def get_recharge(db:Session, idRecharge: int):
    return db.query(models.Recharge).filter(models.Recharge.idRecharge == idRecharge).first() 


def _kw_recharger(montant, total_kw_historic):
    n_kw = 0
    # Si on est toujours sur la premiere tranche
    if total_kw_historic <= variable.LIMIT_KW_TRANCHE_1 :
        m = (variable.LIMIT_KW_TRANCHE_1 - total_kw_historic) * variable.PRIX_KW_TRANCHE_1
        if montant > m:
            n_kw += m / variable.PRIX_KW_TRANCHE_1
            montant -= m
            total_kw_historic += n_kw
        else:
            n_kw += montant / variable.PRIX_KW_TRANCHE_1
            montant = 0
    # Deuxieme tranche
    if montant > 0:
        if total_kw_historic <= variable.LIMIT_KW_TRANCHE_2:
            m = (variable.LIMIT_KW_TRANCHE_2 - total_kw_historic) * variable.PRIX_KW_TRANCHE_2
            if montant > m:
                n_kw += m / variable.PRIX_KW_TRANCHE_2
                # Troisieme tranche
                montant = montant - (montant*variable.TVA + m)
                n_kw += montant / variable.PRIX_KW_TRANCHE_3
            else:
                n_kw += montant / variable.PRIX_KW_TRANCHE_2
                montant = 0
        # Troisieme tranche
        else:
                montant -= montant*variable.TVA
                n_kw += montant / variable.PRIX_KW_TRANCHE_3      
    return round(n_kw, 1)


def set_quantite_kw_recharge(montant, sum_kw_current_month):
    # Le taxe communal est déduit pour tout recharge.
    montant_deduit = montant * variable.TAXE_COMMUNAL
    # Si il s'agit de la premiere recharge du mois on deduit la redevance.
    if sum_kw_current_month == 0:
        montant_deduit += variable.REDEVANCE
    montant -= montant_deduit
    return _kw_recharger(montant, sum_kw_current_month)


def add_recharge(db:Session, recharge:RechargeNew):
    month_sum_recharge = get_sum_recharge_current_month(db=db, numeroCompteur=recharge.numeroCompteur)
    nb_kw = set_quantite_kw_recharge(recharge.montantRecharge, month_sum_recharge['quantiteRecharge'])
    new_recharge_quantite = RechargeQuantiteResponse(**recharge.model_dump(),  quantiteRecharge=nb_kw)
    db_recharge = models.Recharge(**new_recharge_quantite.model_dump())
    db_recharge.dateRecharge = datetime.now()
    db.add(db_recharge)
    db_recharge.codeRecharge = generate_code_recharge()
    db.commit()
    db.refresh(db_recharge)
    return db_recharge


def get_recharge_with_code(db:Session, numeroCompteur:int, codeRecharge:str):
    return db.query(models.Recharge).filter(models.Recharge.numeroCompteur==numeroCompteur,
                                            models.Recharge.codeRecharge==codeRecharge).first()


def update_recharge_status(db:Session, db_recharge:RechargeUpdateResponse):
    if db_recharge.statusRecharge == False:
        db_recharge.statusRecharge = True
        db_compteur = compteur.get_compteur(db=db, numeroCompteur=db_recharge.numeroCompteur)
        if db_compteur:
            db_compteur.totalKwDispo += db_recharge.quantiteRecharge
        db_recharge.dateRechargeUpdate = datetime.now()
        print(db_recharge)
        db.commit()
        db.refresh(db_compteur)
        db.refresh(db_recharge)
        return db_recharge

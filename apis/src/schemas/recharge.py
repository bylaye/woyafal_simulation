from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class RechargeStatus(BaseModel):
    statusRecharge: Optional[bool] = False


class RechargeDate(BaseModel):
    dateRechargeUpdate: Optional[datetime] = datetime.now()


class RechargeCompteur(BaseModel):
    numeroCompteur: int


class RechargeMontant(BaseModel):
    montantRecharge: float


class RechargeQuantite(BaseModel):
    quantiteRecharge: float = 0


class RechargeCode(BaseModel):
    codeRecharge: str


class RechargeBase(RechargeCompteur, RechargeMontant):
    pass


class RechargeNewDate(BaseModel):
    dateRecharge: Optional[datetime] = datetime.now()


class RechargeNew(RechargeBase):
    pass


class RechargeQuantiteResponse(RechargeBase, RechargeQuantite):
    pass


class Recharge(RechargeStatus, RechargeNewDate, RechargeCode, RechargeQuantiteResponse):
    idRecharge: int
    


class RechargeUpdateResponse(RechargeDate, Recharge):
    pass

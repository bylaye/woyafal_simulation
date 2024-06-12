from pydantic import BaseModel
from typing import Optional
from ..config import variable

class TypeCompteurBase(BaseModel):
    immatricule: str
    tva: Optional[float] = variable.TVA
    redevance: Optional[float] = variable.REDEVANCE
    taxeCommunal: Optional[float] = variable.TAXE_COMMUNAL
    limitKwTranche1: float = variable.LIMIT_KW_TRANCHE_1
    prixKwTranche1: float = variable.PRIX_KW_TRANCHE_1
    limitKwTranche2: float = variable.LIMIT_KW_TRANCHE_2
    prixKwTranche2: float = variable.PRIX_KW_TRANCHE_2
    prixKwTranche3: float = variable.PRIX_KW_TRANCHE_3


class TypeCompteurNew(TypeCompteurBase):
    pass 


class TypeCompteur(TypeCompteurBase):
    pass
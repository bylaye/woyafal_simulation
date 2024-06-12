from .mydatabase import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Integer, BigInteger
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean
from datetime import datetime
from src.config import variable


class TypeCompteur(Base):
    __tablename__ = 'TypeCompteur'
    immatricule = Column(String(5), primary_key=True, 
                         comment='code identifiant le type de compteur commercial, domestique, ...')
    tva = Column(Float, nullable=False, default=variable.TVA)
    redevance = Column(Float, nullable=False, default=variable.REDEVANCE)
    taxeCommunal = Column(Float, nullable=False, default=variable.TAXE_COMMUNAL)
    limitKwTranche1 = Column(Float, nullable=False, default=variable.LIMIT_KW_TRANCHE_1)
    prixKwTranche1 = Column(Float, nullable=False, default=variable.PRIX_KW_TRANCHE_1)
    limitKwTranche2 = Column(Float, nullable=False, default=variable.LIMIT_KW_TRANCHE_2)
    prixKwTranche2 = Column(Float, nullable=False, default=variable.PRIX_KW_TRANCHE_2)
    prixKwTranche3 = Column(Float, nullable=False, default=variable.PRIX_KW_TRANCHE_3)
    compteurType = relationship("Compteur", back_populates="typeCompteur")


class Compteur(Base):
    __tablename__ = 'Compteur'
    numeroCompteur = Column(BigInteger, primary_key=True)
    prenom = Column(String(40))
    nom = Column(String(40))
    adresse = Column(String(50))
    typeCompteur = Column(String(20))
    dateAcquisition = Column(DateTime)
    statusCompteur =  Column(Boolean, default=True)
    immatricule = Column(String(5), ForeignKey('TypeCompteur.immatricule'), nullable=False)
    totalKwDispo = Column(Float, nullable=False,  default=0.0)
    creditUrgence = Column(Boolean, nullable=False, default=False)
    recharge = relationship("Recharge",  back_populates="compteur")
    consommation = relationship("Consommation",  back_populates="compteurConso")
    typeCompteur = relationship("TypeCompteur",  back_populates="compteurType")
    #consommationDispo = relationship("ConsoDispo",  back_populates="compteurConsoDispo")


class Recharge(Base):
    __tablename__ = 'Recharge'
    idRecharge = Column(Integer, primary_key=True)
    statusRecharge =  Column(Boolean, nullable=False, default=False)
    quantiteRecharge = Column(Float, nullable=False)
    codeRecharge = Column(String(20),  nullable=False)
    montantRecharge = Column(Float, nullable=False)
    dateRecharge = Column(DateTime, nullable=False, index=True, default=datetime.now())
    dateRechargeUpdate = Column(DateTime)
    numeroCompteur = Column(BigInteger, ForeignKey('Compteur.numeroCompteur'), nullable=False)
    compteur = relationship("Compteur",  back_populates="recharge")


class Consommation(Base):
    __tablename__ = 'Consommation'
    idConso = Column(Integer, primary_key=True)
    numeroCompteur = Column(BigInteger, ForeignKey('Compteur.numeroCompteur'))
    dateConso = Column(DateTime, nullable=False)
    quantiteConso = Column(Float, nullable=False)
    compteurConso = relationship("Compteur",  back_populates="consommation")


# class ConsoDispo(Base):
#     __tablename__ = 'ConsoDispo'
#     numeroCompteur = Column(BigInteger, ForeignKey('Compteur.numeroCompteur'), primary_key=True)
#     totalKwDispo = Column(Float, nullable=False,  default=0.0)
#     creditUrgence = Column(Boolean, nullable=False, default=False)
#     compteurConsoDispo = relationship("Compteur",  back_populates="consommationDispo")
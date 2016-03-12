#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Définition de la classe 'Zone'. Fait partie du paquet des modèles.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""
__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'

from sqlalchemy import *
from modeles.base import Base
from sqlalchemy.orm import relationship, backref, sessionmaker

class Zone(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Est une classe abstraite qui contient les
            informations de base communes à tous les types de zones.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            nom (String) : Nom de la zone.
            position_x (String) : Attribut CSS de la position horizontale de la zone (ex: "10%"). 
            position_y (String) : Attribut CSS de la position verticale de la zone (ex: "10%"). 
            largeur (String) : Attribut CSS de la largeur de la zone (ex: "10%").
            hauteur (String) : Attribut CSS de la hauteur de la zone (ex: "10%").
            type (String) : Type polymorphique de la zone (voir l'attribut '__mapper_args___').
            id_fenetre (Integer) : Référence à l'identifiant d'un objet 'Fenetre'.
            fenetre (Relationship) : Référence à l'objet 'Fenetre' associé. La fonction 'backref'
                crée une liste d'objets 'Zone' dans cet objet.
            __mapper_args__ (Dictionary) : Contient les options qui configurent le polymorphisme de
                la classe.
    """
    __tablename__ = 'Zones'
    id = Column(Integer, primary_key=True)
    nom = Column(String, default='Zone sans nom')
    position_x = Column(Integer, default=50)
    position_y = Column(Integer, default=50)
    position_z = Column(Integer, default=0)
    largeur = Column(Integer, default=10)
    hauteur = Column(Integer, default=10)
    type = Column(String(50))
    id_fenetre = Column(Integer, ForeignKey('Fenetres.id', onupdate='cascade', ondelete='cascade'))
    fenetre = relationship(
        "Fenetre", 
        backref=backref(
            'zones', 
            uselist=True, 
            cascade='delete,all')
        )

    __mapper_args__ = {
        'polymorphic_identity':'Zone',
        'polymorphic_on':type
    }
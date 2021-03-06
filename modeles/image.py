#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Définition de la classe 'Image'. Fait partie du paquet des modèles.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""
__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'

from sqlalchemy import *
from modeles.base import Base
from modeles.media import Media
from sqlalchemy.orm import relationship, backref, sessionmaker

class Image(Media):
    """
        Description: 
            Hérite de la classe 'Media'. Permet de différencier un média de type 'Image' des autres
            types.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Référence à l'identifiant unique d'un 'Media'.
            __mapper_args__ (Dictionary) : Contient les options qui configurent le polymorphisme de
                la classe.
    """
    __tablename__ = 'Images'
    id = Column(
        Integer, 
        ForeignKey('Medias.id', onupdate="cascade", ondelete="cascade"), 
        primary_key=True
        )
    
    __mapper_args__ = {
        'polymorphic_identity':'Image'
    }

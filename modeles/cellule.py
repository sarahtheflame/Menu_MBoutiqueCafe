#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Définition de la classe 'Cellule'. Fait partie du paquet des modèles.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""
__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'

from sqlalchemy import *
from modeles.base import Base
from sqlalchemy.orm import relationship, backref, sessionmaker

class Cellule(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Correspond à une cellule d'une 'Ligne'.
        
        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            contenu (String) : Texte contenu dans la cellule.
            id_ligne_table (Integer) : Référence à l'identifiant d'un objet 'Ligne'.
            id_style (Integer) : Référence à l'identifiant d'un objet 'Style'.
            ligne (Relationship) : Référence à l'objet 'Ligne' associé. La fonction 'backref' crée 
                une liste d'objets 'Cellule' dans cet objet.
            style (Relationship) : Référence à l'objet 'Style' associé.
    """
    __tablename__ = 'Cellules'
    id = Column(Integer, primary_key=True)
    contenu = Column(String(150), default="")
    id_ligne = Column(Integer, ForeignKey('Lignes.id', onupdate='cascade', ondelete='cascade'))
    type_style = Column(String, default="tableau_texte")
    ligne = relationship(
        "Ligne", 
        backref=backref(
            'cellules', 
            uselist=True, 
            cascade='delete,all'),
        foreign_keys=[id_ligne]
        )

    def serialiser_en_json(self):
        """
            Retourne un 'Dict' en format 'JSON' contenant les attributs de la classe (Nécessaire 
            puisque SQLAlchemy modifie l'architecture du '__dict__' de l'objet)
        """
        return dict(
            id = self.id,
            contenu = self.contenu,
            type_style = self.type_style
            )

    def deserialiser_de_json(self, session, data):
        """
            Assigne la valeur des attributs de l'objet à l'aide d'un 'dict' contenant les valeurs 
            à assigner.

            Arguments:
                session (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python 
                                    à la base de données.
                data (Dict) : Dictionnaire qui contient les valeurs à assigner.
        """
        if data.get('contenu') != None : self.contenu = data['contenu']
        if data.get('type_style') != None : self.type_style = data['type_style']

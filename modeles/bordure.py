#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Définition de la classe 'Bordure'. Fait partie du paquet des modèles.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""
__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'

from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Bordure(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Représente des attributs CSS utilisés pour
            définir l'apparence de la bordure d'un objet 'Style'.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            taille (String) : Attribut CSS de la taille (ex: "1px").
            style (String) : Attribut CSS du style (valeurs: "none|hidden|dotted|dashed|solid|..
                ..double|groove|ridge|inset|outset|initial|inherit").
            couleur (String) : Attribut CSS de la couleur et de l'opacité 
                (ex: "rgba(0, 0, 0, 0.8)").
    """
    __tablename__ = 'Bordures'
    id = Column(Integer, primary_key=True)
    taille = Column(String(250), default='0px')
    style = Column(String(250), default='solid')
    couleur = Column(String(250), default='#000000')

    def serialiser_en_json(self):
        """
            Retourne un 'Dict' en format 'JSON' contenant les attributs de la classe (Nécessaire 
            puisque SQLAlchemy modifie l'architecture du '__dict__' de l'objet)
        """
        return dict(
            id = self.id,
            taille = self.taille,
            style = self.style,
            couleur = self.couleur
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
        if data.get('taille') != None : self.taille = data['taille']
        if data.get('style') != None : self.style = data['style']
        if data.get('couleur') != None : self.couleur = data['couleur']

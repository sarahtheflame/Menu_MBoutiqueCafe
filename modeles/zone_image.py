#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Définition de la classe 'ZoneVideo'. Fait partie du paquet des modèles.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""

from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ZoneImage(Zone):
    """
        Description: 
            La classe 'ZoneImage' hérite de la classe 'Zone'. Contient une 'Image'.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Référence à l'identifiant unique d'une 'Zone'.
            id_image (Integer) : Référence à l'identifiant d'un objet 'Image'.
            image (Relationship) : Référence à l'objet 'Image' associé. Dans cet objet, la fonction
                'backref' crée une liste des 'ZoneImage' qui l'utilisent.
            __mapper_args__ (Dictionary) : Contient les options qui configurent le polymorphisme de
                la classe.
    """
    __tablename__ = 'ZonesImage'
    id = Column(
        Integer, 
        ForeignKey('Zones.id', onupdate='cascade', ondelete='cascade'), 
        primary_key=True
        )
    id_image = Column(
        Integer, 
        ForeignKey('Images.id', onupdate='cascade', ondelete='cascade')
        )
    image = relationship(
        Image, 
        backref=backref('zones_images', uselist=True, cascade='delete,all'),
        foreign_keys=[id_image]
        )

    __mapper_args__ = {
        'polymorphic_identity':'ZoneImage',
    }

    def serialiser_en_json(self):
        """
            Retourne un 'Dict' en format 'JSON' contenant les attributs de la classe (Nécessaire 
            puisque SQLAlchemy modifie l'architecture du '__dict__' de l'objet)
        """
        return dict(
            id = self.id,
            nom = self.nom,
            position_x = self.position_x,
            position_y = self.position_y,
            largeur = self.largeur,
            hauteur = self.hauteur,
            type = self.type,
            image = self.image.serialiser_en_json()
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
        if (self.id_image != data['image']['id']):
            self.image = session.query(Image).filter(Image.id == data['image']['id']).one()
        if data.get('nom') != None : self.nom = data['nom']
        if data.get('position_x') != None : self.position_x = data['position_x']
        if data.get('position_y') != None : self.position_y = data['position_y']
        if data.get('largeur') != None : self.largeur = data['largeur']
        if data.get('hauteur') != None : self.hauteur = data['hauteur']
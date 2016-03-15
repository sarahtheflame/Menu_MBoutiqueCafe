#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Définition de la classe 'ZoneVideo'. Fait partie du paquet des modèles.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""
__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'

from sqlalchemy import *
from modeles.base import Base
from modeles.zone import Zone
from modeles.video import Video
from sqlalchemy.orm import relationship, backref, sessionmaker

class ZoneVideo(Zone):
    """
        Description: 
            Hérite de la classe 'Zone'. Contient un 'Video'.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Référence à l'identifiant unique d'une 'Zone'.
            id_video (Integer) : Référence à l'identifiant d'un objet 'Video'
            video (Relationship) : Référence à l'objet 'Video' associé. Dans cet objet, la fonction
                'backref' crée une liste des 'ZoneVideo' qui l'utilisent.
            __mapper_args__ (Dictionary) : Contient les options qui configurent le polymorphisme de
                la classe.
    """
    __tablename__ = 'ZonesVideo'
    id = Column(
        Integer, 
        ForeignKey('Zones.id', onupdate='cascade', ondelete='cascade'), 
        primary_key=True
        )
    id_video = Column(
        Integer, 
        ForeignKey('Videos.id', onupdate='cascade', ondelete='cascade'),
        default=1
        )
    video = relationship(
        "Video", 
        backref=backref('zones_videos', uselist=True, cascade='delete,all'),
        foreign_keys=[id_video]
        )

    __mapper_args__ = {
        'polymorphic_identity':'ZoneVideo',
    }

    def serialiser_en_json(self):
        """
            Retourne un 'Dict' en format 'JSON' contenant les attributs de la classe (Nécessaire 
            puisque SQLAlchemy modifie l'architecture du '__dict__' de l'objet)
        """
        results = dict(
            id = self.id,
            nom = self.nom,
            position_x = self.position_x,
            position_y = self.position_y,
            position_z = self.position_z,
            largeur = self.largeur,
            hauteur = self.hauteur,
            type = self.type,
            video = "undefined"
            )
        if self.video != None: 
            results['video'] = self.video.serialiser_en_json()
        return results

    def deserialiser_de_json(self, session, data):
        """
            Assigne la valeur des attributs de l'objet à l'aide d'un 'dict' contenant les valeurs 
            à assigner.

            Arguments:
                session (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python 
                                    à la base de données.
                data (Dict) : Dictionnaire qui contient les valeurs à assigner.
        """
        if data.get('video') != None:
            if data['video'] != "undefined":
                if (self.id_video != data['video']['id']):
                    self.video = session.query(Video).filter(Video.id == data['video']['id']).one()
        else:
            self.video = session.query(Video).filter(Video.id == 1).one()
        if data.get('nom') != None: 
            if data['nom'] != "" :
                self.nom = data['nom']
        if data.get('position_x') != None : 
            try:
                temp = float(data['position_x'])
                if (temp <= 100 and temp > 0):
                    self.position_x = temp
            except:
                print("Impossible d'enregistrer la valeur car celle-ci ne correspond pas à un float")
        if data.get('position_y') != None : 
            try:
                temp = float(data['position_y'])
                if (temp <= 100 and temp > 0):
                    self.position_y = temp
            except:
                print("Impossible d'enregistrer la valeur car celle-ci ne correspond pas à un float")
        if data.get('position_z') != None : 
            try:
                temp = float(data['position_z'])
                if (temp <= 100 and temp > 0):
                    self.position_z = temp
            except:
                print("Impossible d'enregistrer la valeur car celle-ci ne correspond pas à un float")
        if data.get('largeur') != None : 
            try:
                temp = float(data['largeur'])
                if (temp <= 100 and temp > 5):
                    self.largeur = temp
            except:
                print("Impossible d'enregistrer la valeur car celle-ci ne correspond pas à un float")
        if data.get('hauteur') != None : 
            try:
                temp = float(data['hauteur'])
                if (temp <= 100 and temp > 5):
                    self.hauteur = temp
            except:
                print("Impossible d'enregistrer la valeur car celle-ci ne correspond pas à un float")

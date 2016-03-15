#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Définition de la classe 'ZoneTable'. Fait partie du paquet des modèles.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""
__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'

from sqlalchemy import *
from modeles.base import Base
from modeles.zone import Zone
from modeles.ligne import Ligne
from modeles.cellule import Cellule
from sqlalchemy.orm import relationship, backref, sessionmaker

class ZoneTable(Zone):
    """
        Description: 
            Hérite de la classe 'Zone'. Contient des lignes, qui elles contiennent des cellules, ce 
            qui constitue une table.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Référence à l'identifiant unique d'une 'Zone'.
            id_style (Integer) : Référence à l'identifiant d'un objet 'Style'.
            style (Relationship) : Référence à l'objet 'Style' associé.
            __mapper_args__ (Dictionary) : Contient les options qui configurent le polymorphisme de 
                la classe.
            ** lignes (List) : Liste d'objets 'Ligne' (créée par la fonction 'backref' lancée par la 
                classe 'Ligne').
    """
    __tablename__ = 'ZonesTable'

    id = Column(
        Integer, 
        ForeignKey('Zones.id', onupdate='cascade', ondelete='cascade'), 
        primary_key=True
        )
    nombre_colonnes = Column(Integer, default=1)

    __mapper_args__ = {'polymorphic_identity':'ZoneTable'}

    def serialiser_en_json(self):
        """
            Retourne un 'Dict' en format 'JSON' contenant les attributs de la classe (Nécessaire 
            puisque SQLAlchemy modifie l'architecture du '__dict__' de l'objet)
        """
        lignes_data = []
        data = dict(
            id = self.id,
            nom = self.nom,
            nombre_colonnes = self.nombre_colonnes,
            position_x = self.position_x,
            position_y = self.position_y,
            position_z = self.position_z,
            largeur = self.largeur,
            hauteur = self.hauteur,
            type = self.type
            )
        for ligne in self.lignes:
            lignes_data.append(ligne.serialiser_en_json())
        data['lignes'] = lignes_data
        return data

    def deserialiser_de_json(self, session, data):
        """
            Assigne la valeur des attributs de l'objet à l'aide d'un 'dict' contenant les valeurs 
            à assigner.

            Arguments:
                session (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python 
                                    à la base de données.
                data (Dict) : Dictionnaire qui contient les valeurs à assigner.
        """
        if data.get('nom') != None: 
            if data['nom'] != "" :
                self.nom = data['nom']
        if data.get('nombre_colonnes') != None : self.nombre_colonnes = data['nombre_colonnes']
        if data.get('position_x') != None : 
            try:
                temp = float(data['position_x'])
                if (temp < 100 and temp > 0):
                    self.position_x = temp
            except:
                print("Impossible d'enregistrer la valeur car celle-ci ne correspond pas à un float")
        if data.get('position_y') != None : 
            try:
                temp = float(data['position_y'])
                if (temp < 100 and temp > 0):
                    self.position_y = temp
            except:
                print("Impossible d'enregistrer la valeur car celle-ci ne correspond pas à un float")
        if data.get('position_z') != None : 
            try:
                temp = float(data['position_z'])
                if (temp > 0):
                    self.position_z = temp
            except:
                print("Impossible d'enregistrer la valeur car celle-ci ne correspond pas à un float")
        if data.get('largeur') != None : 
            try:
                temp = float(data['largeur'])
                if (temp < 100 and temp > 5):
                    self.largeur = temp
            except:
                print("Impossible d'enregistrer la valeur car celle-ci ne correspond pas à un float")
        if data.get('hauteur') != None : 
            try:
                temp = float(data['hauteur'])
                if (temp < 100 and temp > 5):
                    self.hauteur = temp
            except:
                print("Impossible d'enregistrer la valeur car celle-ci ne correspond pas à un float")
        if data.get('lignes') != None : 
            for ligne in data['lignes']:
                if (ligne['id'] == 0):
                    nouvelle_ligne = Ligne(zone_table=self)
                    nouvelle_ligne.deserialiser_de_json(session, ligne)
                    session.add(nouvelle_ligne)
                elif ligne['id'] > 0:
                    session.query(Ligne).filter(Ligne.id == ligne['id']).one().deserialiser_de_json(session, ligne)
                elif ligne['id'] < 0:
                    session.delete(session.query(Ligne).filter(Ligne.id == -ligne['id']).one())
                else:
                    print('Impossible de déserialiser la ligne')

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Définition de la classe 'Ligne'. Fait partie du paquet des modèles.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""
__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'

from sqlalchemy import *
from modeles.base import Base
from modeles.cellule import Cellule
from sqlalchemy.orm import relationship, backref, sessionmaker

class Ligne(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Correspond à une ligne d'une 'ZoneTable'.
        
        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            id_zone_table (Integer) : Référence à l'identifiant d'un objet 'ZoneTable'.
            id_style (Integer) : Référence à l'identifiant d'un objet 'Style'.
            zone_table (Relationship) : Référence à l'objet 'ZoneTable' associé. La fonction 
                'backref' crée une liste d'objets 'Ligne' dans cet objet.
            style (Relationship) : Référence à l'objet 'Style' associé.
            ** cellules (List) : Liste d'objets 'Cellule' (créée par la fonction 'backref' lancée 
                par la classe 'Cellule').
    """
    __tablename__ = 'Lignes'
    id = Column(Integer, primary_key=True)
    id_zone_table = Column(
        Integer, 
        ForeignKey('ZonesTable.id', onupdate='cascade', ondelete='cascade')
        )
    zone_table = relationship(
        "ZoneTable", 
        backref=backref(
            'lignes', 
            uselist=True, 
            cascade='delete,all'), 
        foreign_keys=[id_zone_table]
        )

    def serialiser_en_json(self):
        """
            Retourne un 'Dict' en format 'JSON' contenant les attributs de la classe (Nécessaire 
            puisque SQLAlchemy modifie l'architecture du '__dict__' de l'objet)
        """
        cellules_data = []
        data = dict(
            id = self.id
            )
        for cellule in self.cellules:
            cellules_data.append(cellule.serialiser_en_json())
        data['cellules'] = cellules_data
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
        for cellule in data['cellules']:
            if cellule['id'] == 0:
                if len(self.cellules) < self.zone_table.nombre_colonnes:
                    nouvelle_cellule = Cellule(ligne=self)
                    nouvelle_cellule.deserialiser_de_json(session, cellule)
                    session.add(nouvelle_cellule)
            elif cellule['id'] > 0:
                session.query(Cellule).filter(Cellule.id == cellule['id']).one().deserialiser_de_json(session, cellule)
            elif cellule['id'] < 0:
                session.delete(session.query(Cellule).filter(Cellule.id == -cellule['id']).one())
            else:
                print('Impossible de déserialiser la cellule')
    
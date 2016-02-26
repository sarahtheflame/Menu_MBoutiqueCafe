
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Définition de la classe 'ZoneBase'. Fait partie du paquet des modèles.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""
__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'

from sqlalchemy import *
from modeles.base import Base
from modeles.zone import Zone
from sqlalchemy.orm import relationship, backref, sessionmaker

#=========================MODIFIER STYLE POUR REMPLACER PAR TYPE_DE_STYLE (TITRE, ETC)
class ZoneBase(Zone):
    """
        Description: 
            La classe 'ZoneBase' hérite de la classe 'Zone'. Sert à représenter un rectangle
            contenant ou non du texte.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Référence à l'identifiant unique d'une 'Zone'.
            contenu (String) : Texte contenu dans la zone. 
            id_style (Integer) : Référence à l'identifiant d'un objet 'Style'.
            style (Relationship) : Référence à l'objet 'Style' associé.
            __mapper_args__ (Dictionary) : Contient les options qui configurent le polymorphisme de
                la classe.
    """
    __tablename__ = 'ZonesBase'
    id = Column(
        Integer, 
        ForeignKey('Zones.id', onupdate='cascade', ondelete='cascade'), 
        primary_key=True
        )
    contenu = Column(String, default="")
    type_style = Column(String, default="texte")

    def serialiser_en_json(self):
        """
            Retourne un 'Dict' en format 'JSON' contenant les attributs de la classe (Nécessaire 
            puisque SQLAlchemy modifie l'architecture du '__dict__' de l'objet)
        """
        return dict(
            id = self.id,
            contenu = self.contenu,
            nom = self.nom,
            position_x = self.position_x,
            position_y = self.position_y,
            position_z = self.position_z,
            largeur = self.largeur,
            hauteur = self.hauteur,
            type = self.type,
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
        if data.get('nom') != None : self.nom = data['nom']
        if data.get('position_x') != None : self.position_x = data['position_x']
        if data.get('position_y') != None : self.position_y = data['position_y']
        if data.get('position_z') != None : self.position_z = data['position_z']
        if data.get('largeur') != None : self.largeur = data['largeur']
        if data.get('hauteur') != None : self.hauteur = data['hauteur']
        if data.get('type_style') != None : self.type_style = data['type_style']

    __mapper_args__ = {
        'polymorphic_identity':'ZoneBase',
    }
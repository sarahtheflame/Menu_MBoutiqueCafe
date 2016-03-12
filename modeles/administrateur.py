#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Définition de la classe 'Administrateur'. Fait partie du paquet des modèles.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""
__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'

from sqlalchemy import *
from modeles.base import Base
from sqlalchemy.orm import relationship, backref, sessionmaker

class Administrateur(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Sert à l'authentification d'un utilisateur 
            dans le système.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            adresse_courriel (String) : Courriel qui sert à la récupération du mot de passe.
            mot_de_passe (String) : Phrase de sécurité. Est nécessaire pour l'authentification d'un 
                administrateur au système de gestion.
    """
    __tablename__ = 'Administrateurs'
    id = Column(Integer, primary_key=True)
    adresse_courriel = Column(String, default='da.junior.du@gmail.com')
    mot_de_passe = Column(String, default='admin')

    def serialiser_en_json(self):
        """
            Retourne un 'Dict' en format 'JSON' contenant les attributs de la classe (Nécessaire 
            puisque SQLAlchemy modifie l'architecture du '__dict__' de l'objet)
        """
        return dict(
            id = self.id,
            adresse_courriel = self.adresse_courriel,
            mot_de_passe = self.mot_de_passe
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
        if data.get('adresse_courriel') != None : self.adresse_courriel = data['adresse_courriel']
        if data.get('mot_de_passe') != None : self.mot_de_passe = data['mot_de_passe']

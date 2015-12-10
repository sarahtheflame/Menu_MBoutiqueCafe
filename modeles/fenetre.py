#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Définition de la classe 'Fenetre'. Fait partie du paquet des modèles.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""

import theme, image
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Fenetre(Base):
    """
        Description: 
            Représente l'ensemble des informations qui seront utilisées pour générer une page du
            système d'affichage.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            nom (String) : Nom de la fenêtre.
            couleur_fond (String) : Code de couleur hexadécimal représentant la couleur utilisée
                pour le fond.
            id_image_fond (Integer) : Référence à l'identifiant d'un objet 'Image'. Est associé à
                l'attribut 'image_fond'.
            id_theme (Integer) : Référence à l'identifiant d'un objet 'Theme'. Est associé à
                l'attribut 'theme'.
            image_fond (Relationship) : Référence à l'objet 'Image' utilisé pour le fond. 
            theme (Relationship) : Référence à l'objet 'Theme' associé.
            ** zones (List) : Liste d'objets 'Zone' (créée par la fonction 'backref' lancée par la
                classe 'Zone').
    """
    __tablename__ = 'Fenetres'
    id = Column(Integer, primary_key=True)
    nom = Column(String, default="Fenetre sans nom")
    couleur_fond = Column(String, default="#FFFFFF")
    id_image_fond = Column(
        Integer, 
        ForeignKey('Images.id', onupdate="cascade", ondelete="set default"), 
        default=1
        )    # DEFAULT VALIDE??
    id_theme = Column(
        Integer, 
        ForeignKey('Themes.id', onupdate="cascade", ondelete="set default"), 
        default=1
        )  # DEFAULT VALIDE??
    image_fond = relationship(
        Image, 
        foreign_keys=[id_image_fond]
        )
    theme = relationship(
        Theme, 
        backref=backref(
            'fenetres', 
            uselist=True),
        foreign_keys=[id_theme]
        )

    def serialiser_en_json(self):
        """
            Retourne un 'Dict' en format 'JSON' contenant les attributs de la classe (Nécessaire 
            puisque SQLAlchemy modifie l'architecture du '__dict__' de l'objet)
        """
        zones_data = []
        data = dict(
            id = self.id,
            nom = self.nom,
            couleur_fond = self.couleur_fond,
            image_fond = self.image_fond.serialiser_en_json(),
            theme = self.theme.serialiser_en_json()
            )
        for zone in self.zones:
            zones_data.append(zone.serialiser_en_json())
        data['zones'] = zones_data
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
        if data.get('nom') != None : self.nom = data['nom']
        if data.get('couleur_fond') != None : self.couleur_fond = data['couleur_fond']
        if (self.id_theme != data['theme']['id']):
            self.theme = session.query(Theme).filter(Theme.id == data['theme']['id']).one()
        if (self.id_image_fond != data['image_fond']['id']):
            self.image_fond = session.query(Image).filter(Image.id == data['image_fond']['id']).one()
        for zone in data['zones']:
            if zone['id'] == 0:
                if zone['type'] == 'ZoneBase':
                    nouvelle_zone = ZoneBase(fenetre=self)
                    nouvelle_zone.deserialiser_de_json(session, zone)
                    session.add(nouvelle_zone)
                elif zone['type'] == 'ZoneTable':
                    nouvelle_zone = ZoneTable(fenetre=self)
                    nouvelle_zone.deserialiser_de_json(session, zone)
                    session.add(nouvelle_zone)
                elif zone['type'] == 'ZoneImage':
                    nouvelle_zone = ZoneImage(fenetre=self)
                    nouvelle_zone.deserialiser_de_json(session, zone)
                    session.add(nouvelle_zone)
                elif zone['type'] == 'ZoneVideo':
                    nouvelle_zone = ZoneVideo(fenetre=self)
                    nouvelle_zone.deserialiser_de_json(session, zone)
                    session.add(nouvelle_zone)
                else:
                    print("Type de zone inexistante!") # IMPLÉMENTER UNE ERREUR CORRECTE
            elif zone['id'] > 0:
                session.query(Zone).filter(Zone.id == zone['id']).one().deserialiser_de_json(session, zone)
            elif zone['id'] < 0:
                session.delete(session.query(Zone).filter(Zone.id == -zone['id']).one())
            else:
                print('Impossible de déserialiser la zone')

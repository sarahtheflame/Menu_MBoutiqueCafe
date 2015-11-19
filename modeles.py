#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class Media(Base):
    __tablename__ = 'Medias'
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    chemin_fichier = Column(String)
    type = Column(String)

    def serialiser_en_json(self):
        return dict(
            id = self.id,
            nom = self.nom,
            chemin_fichier = self.chemin_fichier,
            type=self.type)

    def deserialiser_de_json(self, data):
        self.nom = data.nom
        self.chemin_fichier = data.chemin_fichier
        self.type = data.type

class Bordure(Base):
    __tablename__ = 'Bordures'
    id = Column(Integer, primary_key=True)
    couleur = Column(String(250))
    taille = Column(String(250))
    style = Column(String(250))

class Style(Base):
    __tablename__ = 'Styles'
    id = Column(Integer, primary_key=True)
    police = Column(String(250))
    couleur = Column(String(250))
    taille = Column(Integer)
    couleur_fond = Column(String(250))
    opacite_fond = Column(Integer)
    gras = Column(String(250))
    italique = Column(String(250))
    bordure_id = Column(
        Integer, 
        ForeignKey('Bordures.id'),
        nullable=False
        )
    bordure = relationship(
        Bordure, 
        uselist=False, 
        cascade='delete,all'
        )

class Theme(Base):
    __tablename__ = 'Themes'
    id = Column(
        Integer, 
        primary_key=True
        )
    nom = Column(
        String(250),
        nullable=False
        )
    id_titre = Column(
        Integer, 
        ForeignKey('Styles.id'),
        nullable=False
        )
    id_sous_titre = Column(
        Integer, 
        ForeignKey('Styles.id'),
        nullable=False
        )
    id_texte = Column(
        Integer, 
        ForeignKey('Styles.id'),
        nullable=False
        )
    id_tableau = Column(
        Integer, 
        ForeignKey('Styles.id'),
        nullable=False
        )
    id_tableau_ligne = Column(
        Integer, 
        ForeignKey('Styles.id'),
        nullable=False
        )
    id_tableau_titre = Column(
        Integer, 
        ForeignKey('Styles.id'),
        nullable=False
        )
    id_tableau_sous_titre = Column(
        Integer, 
        ForeignKey('Styles.id'),
        nullable=False
        )
    id_tableau_texte = Column(
        Integer, 
        ForeignKey('Styles.id'),
        nullable=False
        )

    titre = relationship(
        Style, 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_titre]
        )
    sous_titre = relationship(
        Style, 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_sous_titre]
        )
    texte = relationship(
        Style, 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_texte]
        )
    tableau = relationship(
        Style, 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_tableau]
        )
    tableau_ligne = relationship(
        Style, 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_tableau_ligne]
        )
    tableau_titre = relationship(
        Style, 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_tableau_titre]
        )
    tableau_sous_titre = relationship(
        Style, 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_tableau_sous_titre]
        )
    tableau_texte = relationship(
        Style, 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_tableau_texte]
        )

class Fenetre(Base):
    __tablename__ = 'Fenetres'
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    fond = Column(String)
    id_theme = Column(Integer, ForeignKey('Themes.id'))  
    theme = relationship(Theme, foreign_keys=[id_theme])

    def serialiser_en_json(self):
        return dict(
            id = self.id,
            nom = self.nom,
            fond = self.fond,
            id_theme=self.id_theme)

    def deserialiser_de_json(self, session, data):
        self.nom = data['nom']
        self.fond = data['fond']
        self.theme = session.query(Theme).filter(Theme.id == data['id_theme']).one()
        session.commit()

class Periode(Base):
    __tablename__ = 'Periodes'
    id = Column(Integer, primary_key=True)
    heure_debut = Column(DateTime)
    id_fenetre_1 = Column(Integer, ForeignKey('Fenetres.id'))
    id_fenetre_2 = Column(Integer, ForeignKey('Fenetres.id'))
    id_fenetre_3 = Column(Integer, ForeignKey('Fenetres.id'))
    id_fenetre_4 = Column(Integer, ForeignKey('Fenetres.id'))
    fenetre_1 = relationship(
        Fenetre, 
        uselist=False, 
        foreign_keys=[id_fenetre_1]
        )
    fenetre_2 = relationship(
        Fenetre, 
        uselist=False, 
        foreign_keys=[id_fenetre_2]
        )
    fenetre_3 = relationship(
        Fenetre, 
        uselist=False, 
        foreign_keys=[id_fenetre_3]
        )
    fenetre_4 = relationship(
        Fenetre, 
        uselist=False, 
        foreign_keys=[id_fenetre_4]
        )

class Zone(Base):
    __tablename__ = 'Zones'
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    position_x = Column(String)
    position_y = Column(String)
    largeur = Column(String)
    hauteur = Column(String)
    type = Column(String(50))
    id_fenetre = Column(Integer, ForeignKey('Fenetres.id'))
    fenetre = relationship(
        Fenetre, 
        backref=backref(
            'zones', 
            uselist=True, 
            cascade='delete,all')
        )

    __mapper_args__ = {
        'polymorphic_identity':'Zone',
        'polymorphic_on':type
    }

class ZoneBase(Zone):
    __tablename__ = 'ZonesBase'
    id = Column(Integer, ForeignKey('Zones.id'), primary_key=True)
    contenu = Column(String)
    id_style = Column(Integer, ForeignKey('Styles.id'))
    style = relationship(
        Style,
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_style]
    )

    __mapper_args__ = {
        'polymorphic_identity':'ZoneBase',
    }

class ZoneImage(Zone):
    __tablename__ = 'ZonesImage'
    id = Column(Integer, ForeignKey('Zones.id'), primary_key=True)
    id_media = Column(Integer, ForeignKey('Medias.id'))
    image = relationship(Media)

    __mapper_args__ = {
        'polymorphic_identity':'ZoneImage',
    }

class ZoneVideo(Zone):
    __tablename__ = 'ZonesVideo'
    id = Column(Integer, ForeignKey('Zones.id'), primary_key=True)
    id_media = Column(Integer, ForeignKey('Medias.id'))
    video = relationship(Media)

    __mapper_args__ = {
        'polymorphic_identity':'ZoneVideo',
    }

class ZoneTable(Zone):
    __tablename__ = 'ZonesTable'
    id = Column(Integer, ForeignKey('Zones.id'), primary_key=True)
    id_style = Column(Integer, ForeignKey('Styles.id'))
    style = relationship(
        Style,
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_style]
    )

    __mapper_args__ = {
        'polymorphic_identity':'ZoneTable',
    }

class Ligne(Base):
    __tablename__ = 'Lignes'
    id = Column(Integer, primary_key=True)
    id_zone_table = Column(Integer, ForeignKey('ZonesTable.id'))
    id_style = Column(Integer, ForeignKey('Styles.id'))
    zone_table = relationship(
        ZoneTable, 
        backref=backref(
            'lignes', 
            uselist=True, 
            cascade='delete,all')
        )
    style = relationship(
        Style,
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_style]
    )
    
class Cellule(Base):
    __tablename__ = 'Cellules'
    id = Column(Integer, primary_key=True)
    contenu = Column(String)
    id_ligne_table = Column(Integer, ForeignKey('Lignes.id'))
    id_style = Column(Integer, ForeignKey('Styles.id'))
    ligne = relationship(
        Ligne, 
        backref=backref(
            'cellules', 
            uselist=True, 
            cascade='delete,all')
        )
    style = relationship(
        Style,
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_style]
    )

class Administrateur(Base):
    __tablename__ = 'Administrateurs'
    id = Column(Integer, primary_key=True)
    mot_de_passe = Column(String)
    adresse_courriel = Column(String)

engine = create_engine(
    'sqlite:///src//data//database.db')
Base.metadata.create_all(engine)

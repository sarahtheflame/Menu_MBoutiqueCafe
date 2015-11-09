#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Fenetre(Base):
    __tablename__ = 'Fenetres'
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    fond = Column(String)
    id_theme = Column(Integer, ForeignKey('Themes.id'))  
    theme = relationship(Theme, foreign_keys=[id_theme])

class Periode(Base):
    __tablename__ = 'Periodes'
    id = Column(Integer, primary_key=True)
    heure_debut = Column(DateTime)
    id_fenetre_1 = Column(Integer, ForeignKey('fenetre.id'))  
    id_fenetre_2 = Column(Integer, ForeignKey('fenetre.id'))  
    id_fenetre_3 = Column(Integer, ForeignKey('fenetre.id'))  
    id_fenetre_4 = Column(Integer, ForeignKey('fenetre.id'))
    fenetre_1 = relationship(Fenetre, uselist=False, foreign_keys=[id_fenetre_1])
    fenetre_2 = relationship(Fenetre, uselist=False, foreign_keys=[id_fenetre_2])
    fenetre_3 = relationship(Fenetre, uselist=False, foreign_keys=[id_fenetre_3])
    fenetre_4 = relationship(Fenetre, uselist=False, foreign_keys=[id_fenetre_4])

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
        'polymorphic_identity':'Zones',
        'polymorphic_on':type
    }

class Zone_Base(Zone):
    __tablename__ = 'Zones_Base'
    id = Column(Integer, ForeignKey('Zones.id'), primary_key=True)
    contenu = Column(String)

    __mapper_args__ = {
        'polymorphic_identity':'Zones_Base',
    }

class Zone_Image(Zone):
    __tablename__ = 'Zones_Image'
    id = Column(Integer, ForeignKey('Zones.id'), primary_key=True)
    id_media = Column(Integer, ForeignKey('Medias.id'))
    image = relationship(Media)

    __mapper_args__ = {
        'polymorphic_identity':'Zones_Image',
    }

class Zone_Video(Zone):
    __tablename__ = 'Zones_Video'
    id = Column(Integer, ForeignKey('Zones.id'), primary_key=True)
    id_media = Column(Integer, ForeignKey('Medias.id'))
    video = relationship(Media)

    __mapper_args__ = {
        'polymorphic_identity':'Zones_Video',
    }

class Zone_Table(Zone):
    __tablename__ = 'Zones_Table'
    id = Column(Integer, ForeignKey('Zones.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'Zones_Table',
    }

class Ligne_Table(Base):
    __tablename__ = 'Lignes_Tables'
    id = Column(Integer, primary_key=True)
    id_zone_table = Column(Integer, ForeignKey('Zones_Table.id'))
    id_style = Column(Integer, ForeignKey('Styles.id'))
    zone_table = relationship(
        Zone_Table, 
        backref=backref(
            'lignes', 
            uselist=True, 
            cascade='delete,all')
        )
    
class Cellule_Table(Base):
    __tablename__ = 'Cellules_Table'
    id = Column(Integer, primary_key=True)
    contenu = Column(String)
    id_ligne_table = Column(Integer, ForeignKey('Lignes_Tables.id'))
    id_style = Column(Integer, ForeignKey('Styles.id'))
    ligne_table = relationship(
        Ligne_Table, 
        backref=backref(
            'cellules', 
            uselist=True, 
            cascade='delete,all')
        )

engine = create_engine('sqlite:///src//data//database.db')
Base.metadata.create_all(engine)

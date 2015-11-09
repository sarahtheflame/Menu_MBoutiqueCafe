#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Bordure(Base):
	__tablename__ = 'Bordures'
	id = Column(Integer, primary_key=True)
	couleur = Column(String(250))
	taille = Column(Integer)
	style = Column(String(250))

class Style(Base):
	__tablename__ = 'Styles'
	id = Column(Integer, primary_key=True)
	police = Column(String(250))
	couleur = Column(String(250))
	taille = Column(Integer)
	couleur_fond = Column(String(250))
	opacite = Column(Integer)
	bordure_id = Column(Integer, ForeignKey('Bordures.id'),nullable=False)
	bordure = relationship(Bordure, uselist=False, cascade='delete,all')

class Theme(Base):
	__tablename__ = 'Themes'
	id = Column(Integer, primary_key=True)
	nom = Column(String(250),nullable=False)
	titre_id = Column(Integer, ForeignKey('Styles.id'),nullable=False)
	titre = relationship(Style, uselist=False, cascade='delete,all')
	sous_titre_id = Column(Integer, ForeignKey('Styles.id'),nullable=False)
	sous_titre = relationship(Style, uselist=False, cascade='delete,all')
	texte_id = Column(Integer, ForeignKey('Styles.id'),nullable=False)
	texte = relationship(Style, uselist=False, cascade='delete,all')
	tableau_titre_id = Column(Integer, ForeignKey('Styles.id'),nullable=False)
	tableau_titre = relationship(Style, uselist=False, cascade='delete,all')
	tableau_sous_titre_id = Column(Integer, ForeignKey('Styles.id'),nullable=False)
	tableau_sous_titre = relationship(Style, uselist=False, cascade='delete,all')
	tableau_texte_id = Column(Integer, ForeignKey('Styles.id'),nullable=False)
	tableau_texte = relationship(Style, uselist=False, cascade='delete,all')

engine = create_engine('sqlite:///src///data/database.db')

Base.metadata.create_all(engine)

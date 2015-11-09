#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Periode(Base):
	__tablename__ = 'Periodes'
	id = Column(Integer, primary_key=True)
	heure_debut = Column(DateTime,nullable=False)
	fenetre_1_id = Column(Integer, ForeignKey('Fenetres.id'))
	fenetre_1 = relationship(Fenetre,nullable=False)
	fenetre_2_id = Column(Integer, ForeignKey('Fenetres.id'))
	fenetre_2 = relationship(Fenetre,nullable=False)
	fenetre_3_id = Column(Integer, ForeignKey('Fenetres.id'))
	fenetre_3 = relationship(Fenetre,nullable=False)
	fenetre_4_id = Column(Integer, ForeignKey('Fenetres.id'))
	fenetre_4 = relationship(Fenetre,nullable=False)

engine = create_engine('sqlite:///src///data/database.db')

Base.metadata.create_all(engine)

#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Administrateur(Base):
    __tablename__ = 'Administrateurs'
    id = Column(Integer, primary_key=True)
    mot_de_passe = Column(String)
    adresse_courriel = Column(String)

engine = create_engine('sqlite:///src//data//database.db')
Base.metadata.create_all(engine)

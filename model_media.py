#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Media(Base):
    __tablename__ = 'Medias'
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    chemin_fichier = Column(String)
    type = Column(String)

engine = create_engine('sqlite:///src//data//database.db')
Base.metadata.create_all(engine)
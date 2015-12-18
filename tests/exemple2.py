#!/usr/bin/python
# -*- coding: utf-8 -*-

from modeles_temporaires import *
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json

engine = create_engine('sqlite:///..//src//data//database.db', encoding='utf8', convert_unicode=True)
session = sessionmaker(bind=engine)

s = session()

# EXEMPLE 2 : Modifier le nom d'une fenêtre
fenetre_repas = s.query(Fenetre).filter(Fenetre.id == 1).one()
fenetre_repas.nom = "nouveau nom"
s.commit()
# Résultat : Le nom de la fenêtre a été modifié dans la base de données
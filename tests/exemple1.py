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

# EXEMPLE 1 : Sérialiser une fenêtre
fenetre_repas = s.query(Fenetre).filter(Fenetre.id == 1).one()
json_fenetre = fenetre_repas.serialiser_en_json()
print(json.dumps(json_fenetre, indent=4, separators=(',', ': ')))
# Résultat : Le contenu de la fenêtre sera affiché en format json dans l'invite de commande
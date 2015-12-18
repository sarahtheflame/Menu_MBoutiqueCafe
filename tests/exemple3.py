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

# EXEMPLE 3 : Créer une nouvelle zone dans une fenêtre
fenetre_repas = s.query(Fenetre).filter(Fenetre.id == 1).one()
json_fenetre = fenetre_repas.serialiser_en_json()
nouvelle_zone_base = {
            "id": 0,
            "id_style": 1,
            "type": "ZoneBase"
        }
json_fenetre['zones'].append(nouvelle_zone_base)
fenetre_repas.deserialiser_de_json(s, json_fenetre)
s.commit()
# Résultat : Une nouvelle zone sera ajouté à la liste des zones de la fenetre dont l'identifiant est 1
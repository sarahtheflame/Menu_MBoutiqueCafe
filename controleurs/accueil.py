#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from modeles_temporaires import *

engine = create_engine('sqlite:///..//src//data//database.db', encoding='utf8', convert_unicode=True)
session = sessionmaker(bind=engine)

s = session()

def get_affichage(s, nom_fenetre):
    return s.query(Fenetre).filter(Fenetre.nom == nom_fenetre).one().serialiser_en_json()

def get_gestion(s, nom_vue):
    if nom_vue == "lister_fenetre":
        get_lister_fenetre(s)
    elif nom_vue == "medias":
        get_medias(s)

def get_lister_fenetre(s):
    liste_fenetres = {
        'fenetres' : []
    }
    for fenetre in s.query(Fenetre).all():
        liste_fenetres['fenetres'].append(fenetre.serialiser_en_json())
    return liste_fenetres

def get_medias(s):
    liste_medias = {
        'medias' : []
    }
    for media in s.query(Media).all():
        liste_medias['medias'].append(media.serialiser_en_json())
    print(json.dumps(liste_medias, indent=4, separators=(',', ': ')))
    return liste_medias

get_gestion(s, "medias")
# print(json.dumps(data[0], indent=4, separators=(',', ': ')))

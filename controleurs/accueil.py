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

def get_gestion(s, data):
    if data['nom_vue'] == "lister_fenetres":
        return get_lister_fenetres(s)
    elif data['nom_vue'] == "medias":
        return get_medias(s)
    elif data['nom_vue'] == "themes":
        return get_lister_themes(s)
    elif data['nom_vue'] == "parametres":
        return get_parametres(s)
    elif data['nom_vue'] == "periodes":
        return get_lister_periodes(s)
    elif data['nom_vue'] == "modifier_zone_image":
        return get_modifier_zone_image(s, data['id'])
    elif data['nom_vue'] == "modifier_zone_table":
        return get_modifier_zone_table(s, data['id'])
    elif data['nom_vue'] == "modifier_fenetre":
        return get_modifier_fenetre(s, data['id'])
    elif data['nom_vue'] == "modifier_zone_base":
        return get_modifier_zone_base(s, data['id'])
    elif data['nom_vue'] == "modifier_zone_video":
        return get_modifier_zone_video(s, data['id'])
    elif data['nom_vue'] == "modifier_theme":
        return get_modifier_theme(s, data['id'])

def get_lister_fenetres(s):
    resultats = { 'fenetres' : [] }
    for fenetre in s.query(Fenetre).all():
        resultats['fenetres'].append(fenetre.serialiser_en_json())
    return resultats

def get_medias(s):
    resultats = { 'medias' : [] }
    for media in s.query(Media).all():
        resultats['medias'].append(media.serialiser_en_json())
    return resultats

def get_modifier_theme(s, id_theme):
    resultats = { 
        'theme' : ''
    }
    resultats['theme'] = s.query(Theme).filter(Theme.id == id_theme).one().serialiser_en_json()
    return resultats

def get_lister_themes(s):
    resultats = { 'themes' : [] }
    for theme in s.query(Theme).all():
        resultats['themes'].append(theme.serialiser_en_json())
    return resultats

def get_parametres(s):
    resultats = { 'administrateurs' : [] }
    for administrateur in s.query(Administrateur).all():
        resultats['administrateurs'].append(administrateur.serialiser_en_json())
    return resultats

def get_lister_periodes(s):
    resultats = { 'periodes' : [] }
    for periode in s.query(Periode).all():
        resultats['periodes'].append(periode.serialiser_en_json())
    return resultats

def get_modifier_zone_image(s, id_zone):
    resultats = { 
        'zone_image' : ''
    }
    resultats['zone_image'] = s.query(ZoneImage).filter(ZoneImage.id == id_zone).one().serialiser_en_json()
    return resultats

def get_modifier_zone_video(s, id_zone):
    resultats = { 
        'zone_video' : ''
    }
    resultats['zone_video'] = s.query(ZoneVideo).filter(ZoneVideo.id == id_zone).one().serialiser_en_json()
    return resultats

def get_modifier_zone_table(s, id_zone):
    resultats = { 
        'zone_table' : ''
    }
    resultats['zone_table'] = s.query(ZoneTable).filter(ZoneTable.id == id_zone).one().serialiser_en_json()
    return resultats

def get_modifier_zone_base(s, id_zone):
    resultats = { 
        'zone_base' : ''
    }
    resultats['zone_base'] = s.query(ZoneBase).filter(ZoneBase.id == id_zone).one().serialiser_en_json()
    return resultats

def get_modifier_fenetre(s, id_fenetre):
    resultats = { 
        'fenetre' : ''
    }
    resultats['fenetre'] = s.query(Fenetre).filter(Fenetre.id == id_fenetre).one().serialiser_en_json()
    return resultats

data = get_gestion(s, {'nom_vue' : 'modifier_theme', 'id' : '1'})
print(json.dumps(data, indent=4, separators=(',', ': ')))

# fenetre_repas = s.query(Fenetre).filter(Fenetre.id == 1).one()
# json_fenetre = fenetre_repas.serialiser_en_json()
# print(json.dumps(json_fenetre, indent=4, separators=(',', ': ')))
#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from controleurs.modeles_temporaires import *

def get_affichage(s, nom_fenetre):
    return s.query(Fenetre).filter(Fenetre.nom == nom_fenetre).one().serialiser_en_json()

def get_gestion(s, data):
    if data['nom_vue'] == "lister_fenetres": return get_lister_fenetres(s)
    elif data['nom_vue'] == "medias": return get_medias(s)
    elif data['nom_vue'] == "themes": return get_lister_themes(s)
    elif data['nom_vue'] == "parametres": return get_parametres(s)
    elif data['nom_vue'] == "periodes": return get_lister_periodes(s)
    elif data['nom_vue'] == "modifier_zone_image": return get_modifier_zone_image(s, data['id'])
    elif data['nom_vue'] == "modifier_zone_table": return get_modifier_zone_table(s, data['id'])
    elif data['nom_vue'] == "modifier_fenetre": return get_modifier_fenetre(s, data['id'])
    elif data['nom_vue'] == "modifier_zone_base": return get_modifier_zone_base(s, data['id'])
    elif data['nom_vue'] == "modifier_zone_video": return get_modifier_zone_video(s, data['id'])
    elif data['nom_vue'] == "modifier_theme": return get_modifier_theme(s, data['id'])
    else : raise NameError("Données inexistantes pour la page de gestion demandée!")

def post_gestion(s, data):
    if data['nom_vue'] == "lister_fenetres": return post_lister_fenetres(s)
    elif data['nom_vue'] == "medias": return post_medias(s)
    elif data['nom_vue'] == "themes": return post_lister_themes(s)
    elif data['nom_vue'] == "parametres": return post_parametres(s)
    elif data['nom_vue'] == "periodes": return post_lister_periodes(s)
    elif data['nom_vue'] == "modifier_zone_image": return post_modifier_zone_image(s, data['id'])
    elif data['nom_vue'] == "modifier_zone_table": return post_modifier_zone_table(s, data['id'])
    elif data['nom_vue'] == "modifier_fenetre": return post_modifier_fenetre(s, data['id'])
    elif data['nom_vue'] == "modifier_zone_base": return post_modifier_zone_base(s, data['id'])
    elif data['nom_vue'] == "modifier_zone_video": return post_modifier_zone_video(s, data['id'])
    elif data['nom_vue'] == "modifier_theme": return post_modifier_theme(s, data['id'])
    else : raise NameError("Impossible d'enregistrer les données pour la page de gestion!")

def get_lister_fenetres(s):
    resultats = { 'fenetres' : [], 'themes' : [] }
    for fenetre in s.query(Fenetre).all():
        resultats['fenetres'].append(fenetre.serialiser_en_json())
    for theme in s.query(Theme).all():
        resultats['themes'].append(theme.serialiser_en_json())    
    return resultats

def get_medias(s):
    resultats = { 'medias' : [] }
    for media in s.query(Media).all():
        resultats['medias'].append(media.serialiser_en_json())
    return resultats

def get_modifier_theme(s, id_theme):
    resultats = { 'theme' : '' }
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
    resultats = { 'zone_image' : '' }
    resultats['zone_image'] = s.query(ZoneImage).filter(ZoneImage.id == id_zone).one().serialiser_en_json()
    return resultats

def get_modifier_zone_video(s, id_zone):
    resultats = { 'zone_video' : '' }
    resultats['zone_video'] = s.query(ZoneVideo).filter(ZoneVideo.id == id_zone).one().serialiser_en_json()
    return resultats

def get_modifier_zone_table(s, id_zone):
    resultats = { 'zone_table' : '' }
    resultats['zone_table'] = s.query(ZoneTable).filter(ZoneTable.id == id_zone).one().serialiser_en_json()
    return resultats

def get_modifier_zone_base(s, id_zone):
    resultats = { 'zone_base' : '' }
    resultats['zone_base'] = s.query(ZoneBase).filter(ZoneBase.id == id_zone).one().serialiser_en_json()
    return resultats

def get_modifier_fenetre(s, id_fenetre):
    resultats = { 'fenetre' : '' }
    resultats['fenetre'] = s.query(Fenetre).filter(Fenetre.id == id_fenetre).one().serialiser_en_json()
    return resultats

def post_lister_fenetres(s, data):
    for fenetre in data['fenetres']:
        if fenetre['id'] == 0:
            nouvelle_fenetre = Fenetre()
            nouvelle_fenetre.deserialiser_de_json(s, fenetre)
            s.add(nouvelle_fenetre)
        elif fenetre['id'] > 0:
            s.query(Fenetre).filter(Fenetre.id == fenetre['id']).one().deserialiser_de_json(s, fenetre)
        elif fenetre['id'] < 0:
            s.delete(s.query(Fenetre).filter(Fenetre.id == -fenetre['id']).one())
    return True

def post_medias(s, data):
    for media in data['medias']:
        if media['id'] == 0:
            nouveau_media = Media()
            nouveau_media.deserialiser_de_json(s, media)
            s.add(nouveau_media)
        elif media['id'] > 0:
            s.query(Media).filter(Media.id == media['id']).one().deserialiser_de_json(s, media)
        elif media['id'] < 0:
            s.delete(s.query(Media).filter(Media.id == -media['id']).one())
    return True

def post_modifier_theme(s, data):
    theme = data['theme']
    if theme['id'] == 0:
        nouveau_theme = Theme()
        nouveau_theme.deserialiser_de_json(s, theme)
        s.add(nouveau_theme)
    elif theme['id'] > 0:
        s.query(Theme).filter(Theme.id == theme['id']).one().deserialiser_de_json(s, theme)
    elif theme['id'] < 0:
        s.delete(s.query(Theme).filter(Theme.id == -theme['id']).one())
    return True

def post_lister_themes(s, data):
    for theme in data['themes']:
        if theme['id'] == 0:
            nouveau_theme = Theme()
            nouveau_theme.deserialiser_de_json(s, theme)
            s.add(nouveau_theme)
        elif theme['id'] > 0:
            s.query(Theme).filter(Theme.id == theme['id']).one().deserialiser_de_json(s, theme)
        elif theme['id'] < 0:
            s.delete(s.query(Theme).filter(Theme.id == -theme['id']).one())
    return True

def post_parametres(s, data):
    for administrateur in data['administrateurs']:
        if administrateur['id'] == 0:
            nouvel_administrateur = Administrateur()
            nouvel_administrateur.deserialiser_de_json(s, administrateur)
            s.add(nouvel_administrateur)
        elif administrateur['id'] > 0:
            s.query(Administrateur).filter(Administrateur.id == administrateur['id']).one().deserialiser_de_json(s, administrateur)
        elif administrateur['id'] < 0:
            s.delete(s.query(Administrateur).filter(Administrateur.id == -administrateur['id']).one())
    return True

def post_lister_periodes(s, data):
    for periode in data['periodes']:
        if periode['id'] == 0:
            nouvelle_periode = Periode()
            nouvelle_periode.deserialiser_de_json(s, periode)
            s.add(nouvelle_periode)
        elif periode['id'] > 0:
            s.query(Periode).filter(Periode.id == periode['id']).one().deserialiser_de_json(s, periode)
        elif periode['id'] < 0:
            s.delete(s.query(Periode).filter(Periode.id == -periode['id']).one())
    return True

def post_modifier_zone_image(s, data):
    zone_image = data['zone_image']
    if zone_image['id'] == 0:
        nouvelle_zone_image = ZoneImage()
        nouvelle_zone_image.deserialiser_de_json(s, zone_image)
        s.add(nouvelle_zone_image)
    elif zone_image['id'] > 0:
        s.query(ZoneImage).filter(ZoneImage.id == zone_image['id']).one().deserialiser_de_json(s, zone_image)
    elif zone_image['id'] < 0:
        s.delete(s.query(ZoneImage).filter(ZoneImage.id == -zone_image['id']).one())
    return True

def post_modifier_zone_video(s, data):
    zone_video = data['zone_video']
    if zone_video['id'] == 0:
        nouvelle_zone_video = ZoneVideo()
        nouvelle_zone_video.deserialiser_de_json(s, zone_video)
        s.add(nouvelle_zone_video)
    elif zone_video['id'] > 0:
        s.query(ZoneVideo).filter(ZoneVideo.id == zone_video['id']).one().deserialiser_de_json(s, zone_video)
    elif zone_video['id'] < 0:
        s.delete(s.query(ZoneVideo).filter(ZoneVideo.id == -zone_video['id']).one())
    return True

def post_modifier_zone_table(s, data):
    zone_table = data['zone_table']
    if zone_table['id'] == 0:
        nouvelle_zone_table = ZoneTable()
        nouvelle_zone_table.deserialiser_de_json(s, zone_table)
        s.add(nouvelle_zone_table)
    elif zone_table['id'] > 0:
        s.query(ZoneTable).filter(ZoneTable.id == zone_table['id']).one().deserialiser_de_json(s, zone_table)
    elif zone_table['id'] < 0:
        s.delete(s.query(ZoneTable).filter(ZoneTable.id == -zone_table['id']).one())
    return True

def post_modifier_zone_base(s, data):
    zone_base = data['zone_base']
    if zone_base['id'] == 0:
        nouvelle_zone_base = ZoneBase()
        nouvelle_zone_base.deserialiser_de_json(s, zone_base)
        s.add(nouvelle_zone_base)
    elif zone_base['id'] > 0:
        s.query(ZoneBase).filter(ZoneBase.id == zone_base['id']).one().deserialiser_de_json(s, zone_base)
    elif zone_base['id'] < 0:
        s.delete(s.query(ZoneBase).filter(ZoneBase.id == -zone_base['id']).one())
    return True

def post_modifier_fenetre(s, data):
    fenetre = data['fenetre']
    if fenetre['id'] == 0:
        nouvelle_fenetre = Fenetre()
        nouvelle_fenetre.deserialiser_de_json(s, fenetre)
        s.add(nouvelle_fenetre)
    elif fenetre['id'] > 0:
        s.query(Fenetre).filter(Fenetre.id == fenetre['id']).one().deserialiser_de_json(s, fenetre)
    elif fenetre['id'] < 0:
        s.delete(s.query(Fenetre).filter(Fenetre.id == -fenetre['id']).one())
    return True

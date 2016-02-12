#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from controleurs.modeles_temporaires import *

def est_autorise(s, a_adresse_courriel, a_mot_de_passe):
    # ***** NOTE : Encrypter et Décrypter les informations de connexion *****
    try:
        utilisateur = s.query(Administrateur).filter(Administrateur.adresse_courriel == a_adresse_courriel).one()
        if utilisateur.adresse_courriel == a_adresse_courriel and utilisateur.mot_de_passe == a_mot_de_passe:
            return True
        else:
            raise NameError("Les données de connexion entrées sont invalides!")
    except ValueError:
        raise NameError("Aucun administrateur ne possède cette adresse courriel!")

def get_affichage(s, nom_fenetre):
    return s.query(Fenetre).filter(Fenetre.nom == nom_fenetre).one().serialiser_en_json()

def obtenir_donnees_gestion(s, data):
    if data['nom_vue'] == "accueil": return {'message' : 'Bienvenue!', 'vue_associe' : 'accueil'}
    elif data['nom_vue'] == "lister_fenetres": return get_lister_fenetres(s)
    elif data['nom_vue'] == "medias": return get_medias(s)
    elif data['nom_vue'] == "themes": return get_lister_themes(s)
    elif data['nom_vue'] == "parametres": return get_parametres(s, data['courriel_administrateur'])
    elif data['nom_vue'] == "periodes": return get_lister_periodes(s)
    elif data['nom_vue'] == "modifier_zone": return get_modifier_zone(s, data['id'])
    elif data['nom_vue'] == "modifier_fenetre": return get_modifier_fenetre(s, data['id'])
    elif data['nom_vue'] == "modifier_theme": return get_modifier_theme(s, data['id'])
    elif data['nom_vue'] == "a_propos": return {'vue_associe' : 'a_propos'}
    else : raise NameError("Données inexistantes pour la page de gestion demandée!")

def retourner_donnees_gestion(s, data):
    if data['nom_vue'] == "lister_fenetres": return post_lister_fenetres(s, data['nouvelles_donnees'])
    elif data['nom_vue'] == "medias": return post_medias(s, data['nouvelles_donnees'])
    elif data['nom_vue'] == "themes": return post_lister_themes(s, data['nouvelles_donnees'])
    elif data['nom_vue'] == "parametres": return post_parametres(s, data['nouvelles_donnees'])
    elif data['nom_vue'] == "periodes": return post_lister_periodes(s, data['nouvelles_donnees'])
    elif data['nom_vue'] == "modifier_zone": return post_modifier_zone(s, data['nouvelles_donnees'])
    elif data['nom_vue'] == "modifier_fenetre": return post_modifier_fenetre(s, data['nouvelles_donnees'])
    elif data['nom_vue'] == "modifier_theme": return post_modifier_theme(s, data['nouvelles_donnees'])
    elif data['nom_vue'] == "a_propos": return {}
    else : raise NameError("Impossible d'enregistrer les données pour la page de gestion!")

def get_lister_fenetres(s):
    resultats = { 'fenetres' : [], 'themes' : [], 'vue_associe' : 'lister_fenetres'}
    for fenetre in s.query(Fenetre).order_by(Fenetre.id).all():
        resultats['fenetres'].append(fenetre.serialiser_en_json())
    for theme in s.query(Theme).order_by(Theme.id).all():
        resultats['themes'].append(theme.serialiser_en_json()) 
    return resultats

def get_medias(s):
    resultats = { 'images' : [], 'videos' : [], 'vue_associe' : 'medias'}
    for image in s.query(Image).order_by(Image.id).all():
        resultats['images'].append(image.serialiser_en_json())
    for video in s.query(Video).order_by(Video.id).all():
        resultats['videos'].append(video.serialiser_en_json())
    return resultats

def get_modifier_theme(s, id_theme):
    resultats = { 'theme' : '', 'vue_associe' : 'modifier_theme'}
    resultats['theme'] = s.query(Theme).filter(Theme.id == id_theme).one().serialiser_en_json()
    return resultats

def get_lister_themes(s):
    resultats = { 'themes' : [], 'vue_associe' : 'lister_themes' }
    for theme in s.query(Theme).order_by(Theme.id).all():
        resultats['themes'].append(theme.serialiser_en_json())
    return resultats

def get_parametres(s, courriel_administrateur):
    resultats = { 'administrateur' : [], 'vue_associe' : 'parametres'  }
    resultats['administrateur'] = s.query(Administrateur).filter(Administrateur.adresse_courriel == courriel_administrateur).one().serialiser_en_json()
    return resultats

def get_lister_periodes(s):
    resultats = { 'periodes' : [], 'fenetres' : [], 'vue_associe' : 'lister_periodes'  }
    for periode in s.query(Periode).order_by(Periode.id).all():
        resultats['periodes'].append(periode.serialiser_en_json())
    for fenetre in s.query(Fenetre).order_by(Fenetre.id).all():
        resultats['fenetres'].append(fenetre.serialiser_en_json())
    return resultats

def get_modifier_zone(s, id_zone):
    resultats = { 'zone' : '' }
    type_zone = s.query(Zone).filter(Zone.id == id_zone).one().type
    if type_zone == "ZoneBase":
        resultats['zone'] = s.query(ZoneBase).filter(ZoneBase.id == id_zone).one().serialiser_en_json()
        nom_vue = "modifier_zone_base"
    elif type_zone == "ZoneTable":
        resultats['zone'] = s.query(ZoneTable).filter(ZoneTable.id == id_zone).one().serialiser_en_json()
        nom_vue = "modifier_zone_table"
    elif type_zone == "ZoneImage":
        resultats['zone'] = s.query(ZoneImage).filter(ZoneImage.id == id_zone).one().serialiser_en_json()
        nom_vue = "modifier_zone_image"
    elif type_zone == "ZoneVideo":
        resultats['zone'] = s.query(ZoneVideo).filter(ZoneVideo.id == id_zone).one().serialiser_en_json()
        nom_vue = "modifier_zone_video"
    resultats['vue_associe'] = nom_vue
    return resultats

def get_modifier_fenetre(s, id_fenetre):
    resultats = { 'fenetre' : '','themes': [], 'vue_associe' : 'modifier_fenetre'  }
    for theme in s.query(Theme).order_by(Theme.id).all():
        resultats['themes'].append(theme.serialiser_en_json())
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

def post_modifier_zone(s, data):
    zone = data['zone']
    if zone['id'] == 0:
        nouvelle_zone = Zone()
        if zone['type'] == ZoneBase:
            nouvelle_zone = ZoneBase()
            nouvelle_zone.deserialiser_de_json(s, zone)
        elif zone['type'] == ZoneTable:
            nouvelle_zone = ZoneTable()
            nouvelle_zone.deserialiser_de_json(s, zone)
        elif zone['type'] == ZoneImage:
            nouvelle_zone = ZoneImage()
            nouvelle_zone.deserialiser_de_json(s, zone)
        elif zone['type'] == ZoneVideo:
            nouvelle_zone = ZoneVideo()
            nouvelle_zone.deserialiser_de_json(s, zone)
        s.add(nouvelle_zone)
    elif zone['id'] > 0:
        if zone['type'] == "ZoneBase":
            s.query(ZoneBase).filter(ZoneBase.id == zone['id']).one().deserialiser_de_json(s, zone)
        elif zone['type'] == "ZoneTable":
            s.query(ZoneTable).filter(ZoneTable.id == zone['id']).one().deserialiser_de_json(s, zone)
        elif zone['type'] == "ZoneImage":
            s.query(ZoneImage).filter(ZoneImage.id == zone['id']).one().deserialiser_de_json(s, zone)
        elif zone['type'] == "ZoneVideo":
            s.query(ZoneVideo).filter(ZoneVideo.id == zone['id']).one().deserialiser_de_json(s, zone)
    elif zone['id'] < 0:
        if zone['type'] == ZoneBase:
            s.delete(s.query(ZoneBase).filter(ZoneBase.id == -zone['id']).one())
        elif zone['type'] == ZoneTable:
            s.delete(s.query(ZoneTable).filter(ZoneTable.id == -zone['id']).one())
        elif zone['type'] == ZoneImage:
            s.delete(s.query(ZoneImage).filter(ZoneImage.id == -zone['id']).one())
        elif zone['type'] == ZoneVideo:
            s.delete(s.query(ZoneVideo).filter(ZoneVideo.id == -zone['id']).one())
    else: raise NameError("Le controleur ne peux déserialiser la zone reçu en post") 
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

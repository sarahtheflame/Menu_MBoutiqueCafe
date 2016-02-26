#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from os import path, listdir
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from modeles.media import Media
from modeles.image import Image
from modeles.video import Video
from modeles.bordure import Bordure
from modeles.style import Style
from modeles.theme import Theme
from modeles.fenetre import Fenetre
from modeles.periode import Periode
from modeles.zone import Zone
from modeles.zone_base import ZoneBase
from modeles.zone_image import ZoneImage
from modeles.zone_video import ZoneVideo
from modeles.zone_table import ZoneTable
from modeles.ligne import Ligne
from modeles.cellule import Cellule
from modeles.administrateur import Administrateur
from modeles.base import Base

def est_autorise(s, a_adresse_courriel, a_mot_de_passe):
    """
        Retourne 'True' si un administrateur possédant les informations de connexion 
        'a_adresse_courriel' et 'a_mot_de_passe' existe dans la base de données et 'False' dans le 
        cas contraire.
 
        Argument(s) :
            func (function) : Fonction décorée par le décorateur.
    """
    try:
        utilisateur = s.query(Administrateur).filter(Administrateur.adresse_courriel == a_adresse_courriel).one()
        if utilisateur.adresse_courriel == a_adresse_courriel and utilisateur.mot_de_passe == a_mot_de_passe:
            return True
        else:
            return False
    except ValueError:
        raise NameError("Aucun administrateur ne possède cette adresse courriel!")

def get_affichage(s, id_fenetre):
    """
        Retourne un dictionnaire contenant la fenêtre qui possède 'id_fenetre' comme identifiant 
        ainsi que la liste des polices disponibles dans le serveur.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
            id_fenetre (Integer) : Id de la fenêtre voulue.
    """
    resultats = { 
        'fenetre' : s.query(Fenetre).filter(Fenetre.id == id_fenetre).one().serialiser_en_json(), 
        'polices' : obtenir_noms_polices()
        }
    return resultats

def obtenir_donnees_gestion(s, data):
    """
        Retourne les données de gestion selon la page demandée dans 'data['nom_vue']'.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
            data (Dictionnary) : Dictionnaire en format JSON contenant les informations de la page 
            correspondante à 'data['nom_vue']'.
    """
    if data['nom_vue'] == "accueil": return {'message' : 'Bienvenue!', 'vue_associe' : 'accueil'}
    elif data['nom_vue'] == "lister_fenetres": return get_lister_fenetres(s)
    elif data['nom_vue'] == "medias": return get_medias(s)
    elif data['nom_vue'] == "themes": return get_lister_themes(s)
    elif data['nom_vue'] == "parametres": return get_parametres(s, data['id_administrateur'])
    elif data['nom_vue'] == "periodes": return get_lister_periodes(s)
    elif data['nom_vue'] == "modifier_zone": return get_modifier_zone(s, data['id'])
    elif data['nom_vue'] == "modifier_fenetre": return get_modifier_fenetre(s, data['id'])
    elif data['nom_vue'] == "modifier_theme": return get_modifier_theme(s, data['id'])
    elif data['nom_vue'] == "a_propos": return {'vue_associe' : 'a_propos'}
    else : raise NameError("Données inexistantes pour la page de gestion demandée!")

def retourner_donnees_gestion(s, data):
    """
        Lance la fonction de sauvegarde avec les données reçues du navigateur selon la page du 
        système de gestion.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
            data (Dictionnary) : Dictionnaire en format JSON contenant les informations de la page 
            correspondante à 'data['nom_vue']'.
    """
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
    """
        Obtient les données requises par la page 'lister_fenetre'.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
    """
    resultats = { 'fenetres' : [], 'themes' : [], 'vue_associe' : 'lister_fenetres'}
    for fenetre in s.query(Fenetre).order_by(Fenetre.id).all():
        resultats['fenetres'].append(fenetre.serialiser_en_json())
    for theme in s.query(Theme).order_by(Theme.id).all():
        resultats['themes'].append({
            'id' : theme.id,
            'nom' : theme.nom
            }) 
    return resultats

def get_medias(s):
    """
        Obtient les données requises par la page 'medias'.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
    """
    resultats = { 'images' : [], 'videos' : [], 'vue_associe' : 'medias'}
    for image in s.query(Image).order_by(Image.id).all():
        resultats['images'].append(image.serialiser_en_json())
    for video in s.query(Video).order_by(Video.id).all():
        resultats['videos'].append(video.serialiser_en_json())
    return resultats

def get_modifier_theme(s, id_theme):
    """
        Obtient les données requises par la page 'modifier_theme' du thème possédant l'identifiant 
        'id_theme'.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
    """
    resultats = { 'theme' : '', 'polices' : obtenir_noms_polices(), 'vue_associe' : 'modifier_theme'}
    resultats['theme'] = s.query(Theme).filter(Theme.id == id_theme).one().serialiser_en_json()
    return resultats

def get_lister_themes(s):
    """
        Obtient les données requises par la page 'lister_themes'.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
    """
    resultats = { 'themes' : [], 'vue_associe' : 'lister_themes' }
    for theme in s.query(Theme).order_by(Theme.id).all():
        resultats['themes'].append({
                'id' : theme.id,
                'nom' : theme.nom
            })
    return resultats

def get_parametres(s, id_administrateur):
    """
        Obtient les données requises par la page 'parametres' de l'administrateur possédant 
        l'identifiant 'id_administrateur'.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
    """
    resultats = { 'administrateur' : [], 'vue_associe' : 'parametres'  }
    resultats['administrateur'] = s.query(Administrateur).filter(
        Administrateur.id == id_administrateur).one().serialiser_en_json()
    return resultats

def get_lister_periodes(s):
    """
        Obtient les données requises par la page 'lister_fenetre'.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
    """
    resultats = { 'periodes' : [], 'fenetres' : [], 'vue_associe' : 'lister_periodes'  }
    for periode in s.query(Periode).order_by(Periode.id).all():
        resultats['periodes'].append(periode.serialiser_en_json())
    for fenetre in s.query(Fenetre).order_by(Fenetre.id).all():
        resultats['fenetres'].append({
                'id' : fenetre.id,
                'nom' : fenetre.nom
            })
    return resultats

def get_modifier_zone(s, id_zone):
    """
        Obtient les données requises par la page 'modifier_zone' de la zone possédant l'identifiant 
        'id_zone'.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
    """
    resultats = { 'zone' : '' , 'fenetre_id' : '', 'vue_associe' : ''}
    type_zone = s.query(Zone).filter(Zone.id == id_zone).one().type
    if type_zone == "ZoneBase":
        zone = s.query(ZoneBase).filter(ZoneBase.id == id_zone).one()
        nom_vue = "modifier_zone_base"
    elif type_zone == "ZoneTable":
        zone = s.query(ZoneTable).filter(ZoneTable.id == id_zone).one()
        nom_vue = "modifier_zone_table"
    elif type_zone == "ZoneImage":
        zone = s.query(ZoneImage).filter(ZoneImage.id == id_zone).one()
        nom_vue = "modifier_zone_image"
        resultats['images'] = []
        for image in s.query(Image).order_by(Image.id).all():
            resultats['images'].append(image.serialiser_en_json())
    elif type_zone == "ZoneVideo":
        zone = s.query(ZoneVideo).filter(ZoneVideo.id == id_zone).one()
        nom_vue = "modifier_zone_video"
        resultats['videos'] = []
        for video in s.query(Video).order_by(Video.id).all():
            resultats['videos'].append(video.serialiser_en_json())
    resultats['zone'] = zone.serialiser_en_json()
    resultats['fenetre_id'] = zone.fenetre.id
    resultats['vue_associe'] = nom_vue
    return resultats

def get_modifier_fenetre(s, id_fenetre):
    """
        Obtient les données requises par la page 'modifier_fenetre' de la fenêtre possédant 
        l'identifiant 'id_fenetre'.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
    """
    resultats = { 'fenetre' : '','themes': [], 'images': [], 'zone_focus' : '', 
                        'polices' : obtenir_noms_polices(), 'vue_associe' : 'modifier_fenetre'  }
    for theme in s.query(Theme).order_by(Theme.id).all():
        resultats['themes'].append(theme.serialiser_en_json())
    for image in s.query(Image).order_by(Image.id).all():
        resultats['images'].append(image.serialiser_en_json())
    resultats['fenetre'] = s.query(Fenetre).filter(Fenetre.id == id_fenetre).one().serialiser_en_json()

    return resultats

def post_lister_fenetres(s, data):
    """
        Enregistre les modifications apporté aux informations de la page 'lister_fenetre'.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
            data (Dictionnary) : Dictionnaire en format JSON contenant les informations reçu de la 
            page 'lister_fenetres'.
    """
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
    """
        Enregistre les modifications apporté aux informations de la page 'medias'.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
            data (Dictionnary) : Dictionnaire en format JSON contenant les informations reçu de la 
            page 'medias'.
    """
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
    """
        Enregistre les modifications apporté aux informations de la page 'modifier_theme'.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
            data (Dictionnary) : Dictionnaire en format JSON contenant les informations reçu de la 
            page 'modifier_theme'.
    """
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
    """
        Enregistre les modifications apporté aux informations de la page 'lister_themes'.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
            data (Dictionnary) : Dictionnaire en format JSON contenant les informations reçu de la 
            page 'lister_themes'.
    """
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
    """
        Enregistre les modifications apporté aux informations de la page 'parametres'.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
            data (Dictionnary) : Dictionnaire en format JSON contenant les informations reçu de la 
            page 'parametres'.
    """
    for administrateur in data['administrateurs']:
        if administrateur['id'] == 0:
            nouvel_administrateur = Administrateur()
            nouvel_administrateur.deserialiser_de_json(s, administrateur)
            s.add(nouvel_administrateur)
        elif administrateur['id'] > 0:
            s.query(Administrateur).filter(
                Administrateur.id == administrateur['id']).one().deserialiser_de_json(s, administrateur)
        elif administrateur['id'] < 0:
            s.delete(s.query(Administrateur).filter(Administrateur.id == -administrateur['id']).one())
    return True

def post_lister_periodes(s, data):
    """
        Enregistre les modifications apporté aux informations de la page 'lister_periodes'.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
            data (Dictionnary) : Dictionnaire en format JSON contenant les informations reçu de la 
            page 'lister_periodes'.
    """
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
    """
        Enregistre les modifications apporté aux informations de la page 'modifier_zone'.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
            data (Dictionnary) : Dictionnaire en format JSON contenant les informations reçu de la 
            page 'modifier_zone'.
    """
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

def post_modifier_fenetre(s, data):
    """
        Enregistre les modifications apporté aux informations de la page 'modifier_fenetre'.
 
        Argument(s) :
            s (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
            data (Dictionnary) : Dictionnaire en format JSON contenant les informations reçu de la 
            page 'modifier_fenetre'.
    """
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

def obtenir_noms_polices():
    """
        Retourne une liste contenant les noms de fichiers disponibles dans le répertoire 
        '/src/fonts' sans les extentions de fichier.
 
        Argument(s) :
            ---
    """
    polices = listdir("src//fonts")
    for x in range(0, len(polices)):
        polices[x] = polices[x].split('.')[0]
    return polices

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Fichier principal du projet. Définition des routes du serveur.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""

__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'

import json, os
from bottle import Bottle, error, route, run, request, response, template, static_file, abort, get, post, parse_auth, HTTPError
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from os.path import join, dirname, isfile, abspath
from controleurs.controleur import *
from controleurs.modeles_temporaires import *
from functools import wraps
# from modeles.media import *
# from modeles.image import *
# from modeles.video import *
# from modeles.bordure import *
# from modeles.style import *
# from modeles.theme import *
# from modeles.fenetre import *
# from modeles.periode import *
# from modeles.zone import *
# from modeles.zone_base import *
# from modeles.zone_image import *
# from modeles.zone_video import *
# from modeles.zone_table import *
# from modeles.ligne import *
# from modeles.cellule import *
# from modeles.administrateur import *

appPath = dirname(abspath(__file__)).replace("\\", "\\\\") # Représente le chemin vers le répertoire racine du système.
app = Bottle() # Représente l'application qui gère les routes de notre système.

Base = declarative_base()
engine = create_engine('sqlite:///src//data//database.db')

plugin = sqlalchemy.Plugin(engine, keyword='db', commit=True, use_kwargs=False)

app.install(plugin)
    
#===============================================================================
# Authentification
#===============================================================================

def check_auth(func):
    @wraps(func)
    def check(*args, **kwargs):
        cookie_courriel = request.get_cookie("administrateur", secret="secret_temporaire")
        if cookie_courriel:
            return func(*args, **kwargs)
        else:
            variables = {}
            return template("src\\views\\autre\\connexion.html", variables)
    return check

#===============================================================================
# Page de connexion
#===============================================================================

@app.route('/g/connexion', method='GET')
def get_connexion(db):
    """
        Fonction associée à une route dynamique qui retourne le 'template' de type 
        'html' s'il existe dans le répertoire '<<appPath>>/src/views'.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
    """
    variables = {}
    return template("src\\views\\autre\\connexion.html", variables)

@app.route('/g/connexion', method='POST')
def post_connexion(db):
    """
        Fonction associée à une route dynamique qui retourne le 'template' de type 
        'html' s'il existe dans le répertoire '<<appPath>>/src/views'.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
    """
    variables = {
        'titre' : 'accueil',
        'path' : "src\\views\\gestion\\base_gestion.html",
        'data' : obtenir_donnees_gestion(db, {'nom_vue' : 'accueil'})
    }
    courriel = request.forms.get('courriel')
    mot_de_passe = request.forms.get('mot_de_passe')
    if est_autorise(db, courriel, mot_de_passe):
        response.set_cookie("administrateur", courriel, secret="secret_temporaire")
        return template("src\\views\\gestion\\accueil.html", variables)
    else:
        return template("src\\views\\autre\\connexion.html", variables)

#===============================================================================
# Pages du système de gestion
#===============================================================================

@app.route('/g/<nom_fichier>', method='GET')
@check_auth
def get_gestion(nom_fichier, db):
    """
        Fonction associée à une route dynamique qui retourne le 'template' de type 
        'html' s'il existe dans le répertoire '<<appPath>>/src/views'.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
    """
    donnees_gestion = obtenir_donnees_gestion(db, {
        'nom_vue' : nom_fichier, 
        'id' : request.query.id, 
        'courriel_administrateur' : request.get_cookie("administrateur", secret="secret_temporaire")
    })
    variables = {
        'titre' : nom_fichier,
        'path' : "src\\views\\gestion\\base_gestion.html",
        'data' : donnees_gestion
    }
    return template("src\\views\\gestion\\"+donnees_gestion['vue_associe']+".html", variables)
    
@app.route('/g/<nom_fichier>', method='POST')
@check_auth
def post_gestion(nom_fichier, db):
    """
        Fonction associée à une route dynamique qui retourne le 'template' de type 
        'html' s'il existe dans le répertoire '<<appPath>>/src/views'.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
    """
    variables = {
        'nom_vue' : request.forms.getunicode('fileName'),
        'nouvelles_donnees' : json.loads(request.forms.getunicode('unmapped'))
    }
    retourner_donnees_gestion(db, variables)
    return get_gestion(nom_fichier, db)
    
#===============================================================================
# Pages du système d'affichage
#===============================================================================

@app.route('/a/<id_fenetre>')
def affichage(id_fenetre, db):
    """
        Fonction associée à une route dynamique qui retourne le 'template' de type 
        'html' s'il existe dans le répertoire '<<appPath>>/src/views'.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
    """
    fenetre = db.query(Fenetre).filter(Fenetre.id == id_fenetre).one().serialiser_en_json()
    variables = {
        'titre' : id_fenetre,
        'data' : {'fenetre' : fenetre}
    }
    return template('src\\views\\affichage\\base_affichage.html', variables)
    
#===============================================================================
# Téléchargement de fichier
#===============================================================================

@app.route('/upload', method='POST')
def do_upload(db):
    category   = request.forms.get('category')
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext in ('.png','.jpg','.jpeg'):
        upload.save('src\\images') # appends upload.filename automatically
    return get_gestion("medias", db)

#===============================================================================
# Fichiers statiques
#===============================================================================

@app.route('/src/<nom_fichier:re:.*\.(js|json)>')
def javascripts(nom_fichier):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 
        'javascripts' s'il existe dans le répertoire '<<appPath>>/src/js'.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(nom_fichier, root="src\\js")

@app.route('/src/<nom_fichier:re:.*\.css>')
def stylesheets(nom_fichier):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 
        'stylesheets' s'il existe dans le répertoire '<<appPath>>/src/css'.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(nom_fichier, root="src\\css")

@app.route('/src/<nom_fichier:re:.*\.(jpg|png|gif|ico|jpeg)>')
def images(nom_fichier):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 'images' 
        s'il existe dans le répertoire '<<appPath>>/src/images'.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(nom_fichier, root="src\\images")

@app.route('/src/<nom_fichier:re:.*\.(mp4)>')
def videos(nom_fichier):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 'videos' 
        s'il existe dans le répertoire '<<appPath>>/src/videos'.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(nom_fichier, root="src\\videos")

@app.route('/src/<nom_fichier:re:.*\.(eot|ttf|woff|svg)>')
def fonts(nom_fichier):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 'fonts' 
        s'il existe dans le répertoire '<<appPath>>/src/fonts'.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(nom_fichier, root="src\\fonts")

#===============================================================================
# Erreurs
#===============================================================================

@app.error(404)
def notFound(error):
    """
        Fonction associée à une route inconnue au système (Erreur 404).

        Argument(s) :
            error (?) : ---
    """
    return '<h1>Erreur 404</h1>'

#===============================================================================
# Lancement de l'application 'app' sur le port '80' de l'hébergeur '0.0.0.0' (localhost) en mode 
# 'debug'.
#===============================================================================

if __name__ == "__main__":
    run(app, host='0.0.0.0', port=80, debug=True)
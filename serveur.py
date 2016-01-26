#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Fichier principal du projet. Définition des routes du serveur.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""

__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'

import json
from bottle import Bottle, error, route, run, request, response, template, static_file, abort, get, post, parse_auth, HTTPError
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from os.path import join, dirname, isfile, abspath
from controleurs.controleur import *
from controleurs.modeles_temporaires import *
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
engine = create_engine('sqlite:///src//data//database.db', encoding='utf8', convert_unicode=True)

plugin = sqlalchemy.Plugin(
    engine,
    keyword='db',
    commit=True,
    use_kwargs=False
)
app.install(plugin)

@app.route('/g/<filename>')
def gestion(filename, db):
    """
        Fonction associée à une route dynamique qui retourne le 'template' de type 
        'html' s'il existe dans le répertoire '<<appPath>>/src/views'.

        Argument(s) :
            filename (String) : Nom du fichier entrée dans l'URL
    """
    path = "src\\views\\gestion\\base_gestion.html"
    variables = {
        'titre' : filename,
        'path' : path,
        'data' : get_gestion(db, {'nom_vue' : filename})
    }
    return template("src\\views\\gestion\\"+filename+".html", variables)

@app.route('/a/<nom_fenetre>')
def affichage(nom_fenetre, db):
    """
        Fonction associée à une route dynamique qui retourne le 'template' de type 
        'html' s'il existe dans le répertoire '<<appPath>>/src/views'.

        Argument(s) :
            filename (String) : Nom du fichier entrée dans l'URL
    """
    fenetre = db.query(Fenetre).filter(Fenetre.nom == nom_fenetre).one().serialiser_en_json()
    variables = {
        'titre' : nom_fenetre,
        'fenetre' : fenetre
    }
    return template('src\\views\\affichage\\base_affichage.html', variables)

@app.route('/src/<filename:re:.*\.(js|json)>')
def javascripts(filename):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 
        'javascripts' s'il existe dans le répertoire '<<appPath>>/src/js'.

        Argument(s) :
            filename (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(filename, root="src\\js")

@app.route('/src/<filename:re:.*\.css>')
def stylesheets(filename):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 
        'stylesheets' s'il existe dans le répertoire '<<appPath>>/src/css'.

        Argument(s) :
            filename (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(filename, root="src\\css")

@app.route('/src/<filename:re:.*\.(jpg|png|gif|ico|jpeg)>')
def images(filename):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 'images' 
        s'il existe dans le répertoire '<<appPath>>/src/images'.

        Argument(s) :
            filename (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(filename, root="src\\images")

@app.route('/src/<filename:re:.*\.(mp4)>')
def videos(filename):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 'videos' 
        s'il existe dans le répertoire '<<appPath>>/src/videos'.

        Argument(s) :
            filename (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(filename, root="src\\videos")

@app.route('/src/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 'fonts' 
        s'il existe dans le répertoire '<<appPath>>/src/fonts'.

        Argument(s) :
            filename (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(filename, root="src\\fonts")
    
@app.route('/')
def main():
    """
        Exemple de route fonctionnelle.
    """
    return "Page d'exemple!"

@app.error(404)
def notFound(error):
    """
        Fonction associée à une route inconnue au système (Erreur 404).

        Argument(s) :
            error (?) : ---
    """
    return 'Erreur 404'

"""
    Lancement de l'application 'app' sur le port '80' de l'hébergeur '0.0.0.0' (localhost) en mode 
    'debug'.
"""
if __name__ == "__main__":
    run(app, host='0.0.0.0', port=80, debug=True)
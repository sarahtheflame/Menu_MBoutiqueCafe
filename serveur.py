#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Fichier principal du projet. Définition des routes du serveur.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""

__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'

import json
from bottle import Bottle, error, route, run, request, response, template, static_file, abort, get, post, parse_auth
from os.path import join, dirname, isfile, abspath
# from controleur_affichage import *
from modeles_temporaires import *

appPath = dirname(abspath(__file__)).replace("\\", "\\\\") # Représente le chemin vers le répertoire racine du système.
app = Bottle() # Représente l'application qui gère les routes de notre système.
print(appPath)
# --- testing ---
from bottle import HTTPError
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///src//data//database.db', encoding='utf8', convert_unicode=True)

plugin = sqlalchemy.Plugin(
    engine, # SQLAlchemy engine created with create_engine function.
    keyword='db', # Keyword used to inject session database in a route (default 'db').
    commit=True, # If it is true, plugin commit changes after route is executed (default True).
    use_kwargs=False # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
)
app.install(plugin)
# --- testing-end --- 


# DATABASE ENGINE
# engine = create_engine('sqlite:///src//data//database.db', encoding='utf8', convert_unicode=True)
# session = sessionmaker(bind=engine)
# s = session()

# CONTROLEURS
# c_affichage = ControleurAffichage()

@app.route('/g/<filename>')
def gestion(filename):
    """
        Fonction associée à une route dynamique qui retourne le 'template' de type 
        'html' s'il existe dans le répertoire '<<appPath>>/src/views'.

        Argument(s) :
            filename (String) : Nom du fichier entrée dans l'URL
    """
    path = "src\\views\\base_gestion.html"
    data = {
        'titre' : filename,
        'path' : path
    }

    return template("src\\views\\"+filename+".html", data)

@app.route('/a/<nom_fenetre>')
def affichage(nom_fenetre, db):
    """
        Fonction associée à une route dynamique qui retourne le 'template' de type 
        'html' s'il existe dans le répertoire '<<appPath>>/src/views'.

        Argument(s) :
            filename (String) : Nom du fichier entrée dans l'URL
    """
    menu = db.query(Fenetre).filter(Fenetre.nom == nom_fenetre).one().serialiser_en_json()
    data = {
        'titre' : nom_fenetre,
        'menu' : menu
    }
    return template('src\\views\\base_affichage.html', data)

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
    print("ok")
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
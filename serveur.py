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
from os.path import join, dirname, isfile
from controleurs.controleurTest import *
from modeles import *
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

session = sessionmaker(bind=create_engine('sqlite:///..//src//data//database.db', encoding='utf8', convert_unicode=True))
s = session()

controleur_test = ControleurTest(s)

appPath = dirname(__file__)

app = Bottle()

@app.route('/<filename:re:.*\.(js|json)>')
def javascripts(filename):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 'javascripts' s'il existe dans le répertoire '<<appPath>>/src/js'.

        Argument(s) :
            filename (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(filename, root=join(appPath, 'src', 'js'))

@app.route('/<filename:re:.*\.css>')
def stylesheets(filename):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 'stylesheets' s'il existe dans le répertoire '<<appPath>>/src/css'.

        Argument(s) :
            filename (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(filename, root=join(appPath, 'src', 'css'))

@app.route('/<filename:re:.*\.(jpg|png|gif|ico|jpeg)>')
def images(filename):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 'images' s'il existe dans le répertoire '<<appPath>>/src/images'.

        Argument(s) :
            filename (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(filename, root=join(appPath, 'src', 'images'))

@app.route('/<filename:re:.*\.(mp4)>')
def videos(filename):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 'videos' s'il existe dans le répertoire '<<appPath>>/src/videos'.

        Argument(s) :
            filename (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(filename, root=join(appPath, 'src', 'videos'))

@app.route('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 'fonts' s'il existe dans le répertoire '<<appPath>>/src/fonts'.

        Argument(s) :
            filename (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(filename, root=join(appPath, 'src', 'fonts'))
    
# Main Route
@app.route('/')
def main():
    return "Main Page"

@app.route('/repas')
def main():
    return template(join(appPath, 'base_repas.html'))

@app.error(404)
def notFound(error):
    """
        Fonction associée à une route inconnue au système (Erreur 404).

        Argument(s) :
            error (?) : ---
    """
    return 'Erreur 404'


if __name__ == "__main__":
    run(app, host='0.0.0.0', port=80, debug=True)
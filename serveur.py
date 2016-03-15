#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Fichier principal du projet. Définition des routes du serveur.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""

__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "da.junior.du@gmail.com"
__status__ = "Development"

import socket
from gevent import monkey; monkey.patch_all()
import json, os, bottle_sqlalchemy, webbrowser, datetime
from bottle import Bottle, error, route, run, request, response, template, static_file, abort, get, post, parse_auth, HTTPError
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from os.path import join, dirname, isfile, abspath
from controleurs.controleur import *
from functools import wraps
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

# Initialisation de l'application «Bottle»
app = Bottle()

# Installation du plugin «SQLAlchemy» dans l'application de «Bottle»
app.install(sqlalchemy.Plugin(create_engine('sqlite:///src//data//database.db'), keyword='db', 
    commit=True, use_kwargs=False))

# Obtention du port à utiliser par le server via la console
port_choisi = ""
while not port_choisi.isdigit():
    port_choisi = input("Entrez un port sur lequel héberger le serveur : ")

print("\nVoici votre adresse IP : " + socket.gethostbyname(socket.gethostname()) + "\n")

#===============================================================================
# Authentification
#===============================================================================

def verifier_session(func):
    """
        Décorateur de fonction qui vérifie l'authenticité de la session du navigateur.

        Argument(s) :
            func (function) : Fonction décorée par le décorateur.
    """
    @wraps(func)
    def check(*args, **kwargs):
        """
            Fonction lancée par le décorateur sur la fonction décorée.

            Argument(s) :
                func (function) : Fonction décorée par le décorateur.
                *args (Arguments) : Liste d'argument reçu par la fonction décorée. ***
                **kwargs (Arguments) : Liste d'argument reçu par la fonction décorée. ***
        """
        id_administrateur = request.get_cookie("administrateur", 
            secret="JxLZ2UztqHT1MtD72a8T1gmTnXpsvghC0XsR231rdwW8YtLt936N47gQ74PN15Eox")
        print(id_administrateur)
        if id_administrateur and id_administrateur > 0:
            return func(*args, **kwargs)
        else:
            return template("src\\views\\autre\\connexion.html", {})
    return check

#===============================================================================
# Page de connexion
#===============================================================================

@app.route('/g/connexion', method='GET')
def get_connexion(db):
    """
        Fonction associée à une route 'GET' qui retourne le 'template' de type 'html' correspondant 
        à la page de connexion (connexion.html).

        Argument(s) :
            db (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
    """
    variables = {}
    return template("src\\views\\autre\\connexion.html", variables)

@app.route('/g/connexion', method='POST')
def post_connexion(db):
    """
        Fonction associée à une route 'POST' qui retourne le 'template' de type 
        'html' correspondant à la page de connexion (connexion.html) si les informations de connexion 
        sont incorrectes. Sinon, le 'template' de type 'html' correspondant à la page d'accueil 
        (accueil.html) est retournée.

        Argument(s) :
            db (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
    """
    variables = {
        'titre' : 'accueil',
        'path' : "src\\views\\gestion\\base_gestion.html",
        'data' : obtenir_donnees_gestion(db, {'nom_vue' : 'accueil'})
    }
    courriel = request.forms.get('adresse_courriel')
    mot_de_passe = request.forms.get('mot_de_passe')
    if est_autorise(db, courriel, mot_de_passe):
        administrateur = db.query(Administrateur).filter(Administrateur.adresse_courriel == courriel).one()
        response.set_cookie("administrateur", administrateur.id, 
            secret="JxLZ2UztqHT1MtD72a8T1gmTnXpsvghC0XsR231rdwW8YtLt936N47gQ74PN15Eox")
        return template("src\\views\\gestion\\accueil.html", variables)
    else:
        return template("src\\views\\autre\\connexion.html", variables)

@app.route('/g/deconnexion', method='GET')
def deconnexion():
    """
        Fonction associée à une route 'GET' qui retourne le 'template' de type 'html' correspondant 
        à la page de connexion (connexion.html).

        Argument(s) :
            db (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
    """
    id_administrateur = request.get_cookie("administrateur", 0,
            secret="JxLZ2UztqHT1MtD72a8T1gmTnXpsvghC0XsR231rdwW8YtLt936N47gQ74PN15Eox")
    response.set_cookie("administrateur", id_administrateur, secret="...")
    return template("src\\views\\autre\\connexion.html", {})
    
#===============================================================================
# Pages du système de gestion
#===============================================================================

@app.route('/g/<nom_fichier>', method='GET')
@verifier_session
def get_gestion(nom_fichier, db):
    """
        Fonction associée à une route dynamique 'GET' qui retourne le 'template' de type 
        'html' correspondant au fichier '<nom_fichier>.html' s'il existe dans le répertoire 
        '/src/views/gestion'.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
            db (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
    """
    donnees_gestion = obtenir_donnees_gestion(db, {
        'nom_vue' : nom_fichier,
        'id' : request.query.id, 
        'id_administrateur' : request.get_cookie("administrateur", 
            secret="JxLZ2UztqHT1MtD72a8T1gmTnXpsvghC0XsR231rdwW8YtLt936N47gQ74PN15Eox")
    })
    variables = {
        'titre' : nom_fichier,
        'path' : "src\\views\\gestion\\base_gestion.html",
        'data' : donnees_gestion
    }
    return template("src\\views\\gestion\\"+donnees_gestion['vue_associe']+".html", variables)
    
@app.route('/g/<nom_fichier>', method='POST')
@verifier_session
def post_gestion(nom_fichier, db):
    """
        Fonction associée à une route dynamique 'POST' d'une page du système de gestion. Exécute 
        'retourner_donnees_gestion' avec les données reçues par la requête 'POST'.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
            db (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
    """
    variables = {
        'nom_vue' : request.forms.getunicode('fileName'),
        'nouvelles_donnees' : json.loads(request.forms.getunicode('unmapped'))
    }
    retourner_donnees_gestion(db, variables)
    
#===============================================================================
# Pages du système d'affichage
#===============================================================================

@app.route('/a/<id_fenetre>')
def afficher_fenetre(id_fenetre, db):
    """
        Fonction associée à une route dynamique qui retourne le 'template' de type 
        'html' du fichier '<id_fenetre>.html' s'il existe dans le répertoire '/src/views/affichage'.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
            db (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
    """
    variables = {
        'titre' : id_fenetre,
        'data' : get_affichage(db, id_fenetre)
    }
    return template('src\\views\\affichage\\base_affichage.html', variables)

@app.route('/afficher_fenetres', method='POST')
def afficher_fenetres(db):
    """
        Fonction associée à une route 'POST' qui obtient la période actuelle et affiche les fenêtres 
        qui y sont associées dans le navigateur par défaut du système.

        Argument(s) :
            db (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
    """
    now = datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute)
    periode = db.query(Periode).filter(Periode.heure_debut < now).order_by(
        desc(Periode.heure_debut)).first()
    webbrowser.open("http://localhost/a/" + str(periode.id_fenetre_1))
    webbrowser.open("http://localhost/a/" + str(periode.id_fenetre_2))
    webbrowser.open("http://localhost/a/" + str(periode.id_fenetre_3))
    webbrowser.open("http://localhost/a/" + str(periode.id_fenetre_4))
    
#===============================================================================
# Téléchargement de fichier
#===============================================================================

@app.route('/g/televerser', method='POST')
def televerser(db):
    """
        Fonction associée à une route 'POST' qui permet de téléverser des fichiers de type '.png',
        '.jpg','.jpeg' dans le répertoire '/src/images' du serveur et permet de téléverser des 
        fichiers de type '.mp4' dans le répertoire '/src/videos' du serveur.

        Argument(s) :
            db (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python à la base 
            de données.
    """
    try:
        variables = {
            'nom_vue' : 'medias',
            'nouvelles_donnees' : json.loads(request.forms.getunicode('unmapped'))
        }
        retourner_donnees_gestion(db, variables)
    except Exception:
        print("Aucune données 'unmapped'")
    try:
        televersement = request.files.get('fichier')
        nom_fichier, extension = os.path.splitext(televersement.filename)
        if extension in ('.png','.jpg','.jpeg', '.gif'):
            televersement.save('src\\images')
            retourner_donnees_gestion(db, {
                'nom_vue' : 'medias',
                'nouvelles_donnees' : {
                    'images' : [
                        {
                            'id' : 0,
                            'nom' : televersement.filename,
                            'chemin_fichier' : televersement.filename,
                            'type' : 'Image'
                        }
                    ]
                }
            })
        elif extension in ('.mp4'):
            televersement.save('src\\videos')
            retourner_donnees_gestion(db, {
                'nom_vue' : 'medias',
                'nouvelles_donnees' : {
                    'videos' : [
                        {
                            'id' : 0,
                            'nom' : televersement.filename,
                            'chemin_fichier' : televersement.filename,
                            'type' : 'Video'
                        }
                    ]
                }
            })
    except Exception:
        print("Aucun média à téléverser!")
    return get_gestion("medias", db)

#===============================================================================
# Fichiers statiques
#===============================================================================

@app.route('/src/<nom_fichier:re:.*\.(js|json)>')
def javascripts(nom_fichier):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 
        'javascripts' s'il existe dans le répertoire '/src/js' du serveur.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(nom_fichier, root="src\\js")

@app.route('/src/<nom_fichier:re:.*\.css>')
def stylesheets(nom_fichier):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 
        'stylesheets' s'il existe dans le répertoire '/src/css' du serveur.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(nom_fichier, root="src\\css")

@app.route('/src/<nom_fichier:re:.*\.(jpg|png|gif|ico|jpeg|svg)>')
def images(nom_fichier):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 'images' 
        s'il existe dans le répertoire '/src/images' du serveur.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(nom_fichier, root="src\\images")

@app.route('/src/<nom_fichier:re:.*\.(mp4)>')
def videos(nom_fichier):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 'videos' 
        s'il existe dans le répertoire '/src/videos' du serveur.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(nom_fichier, root="src\\videos")

@app.route('/src/<nom_fichier:re:.*\.(eot|ttf|woff|svg)>')
def fonts(nom_fichier):
    """
        Fonction associée à une route dynamique qui retourne le fichier statique de type 'fonts' 
        s'il existe dans le répertoire '/src/fonts' du serveur.

        Argument(s) :
            nom_fichier (String) : Nom du fichier entrée dans l'URL
    """
    return static_file(nom_fichier, root="src\\fonts")

#===============================================================================
# Erreurs
#===============================================================================

@app.error(404)
def erreur_404(error):
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
    run(app, host='0.0.0.0', port=port_choisi, server='gevent', debug=True)
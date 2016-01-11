#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Exemple 1 : Sérialisation d'une fenêtre en JSON
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""
__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'

from tests.modeles_temporaires import *
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json

class ControleurAffichage:
    def __init__(self):
        self.actif = True

    def generer_json(self, s, a_nom_fenetre):
        fenetre_repas = s.query(Fenetre).filter(Fenetre.nom == a_nom_fenetre).one()
        return fenetre_repas.serialiser_en_json()
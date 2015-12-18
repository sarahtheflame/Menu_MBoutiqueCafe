#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Définition de la classe 'ControleurTest'. Fait partie du paquet des controleurs.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 15-12-2015
"""

from controleur_donnees import *

class ControleurTest:
    """

    """
    def __init__(ControleurDonnees):
        """
        
        """
        self.fenetre = session.query(Fenetre).filter(Fenetre.id == 1).one()

    def generer_json(self):
        return self.fenetre.serialiser_en_json()

    def appliquer_modification(self, json):
        try:
            self.fenetre.deserialiser_de_json(json)
            return 0
        except ValueError:
            print("Impossible de deserialiser 'self.fenetre'")
            return 1

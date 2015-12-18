#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Exemple 2 : Modification du nom d'une fenêtre
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""
__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'

from modeles_temporaires import *
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json

engine = create_engine('sqlite:///..//src//data//database.db', encoding='utf8', convert_unicode=True)
session = sessionmaker(bind=engine)

s = session()

fenetre_repas = s.query(Fenetre).filter(Fenetre.id == 1).one()
fenetre_repas.nom = "nouveau nom"
s.commit()

# Résultat : Le nom de la fenêtre dont l'identifiant est 1 a été modifié dans la base de données
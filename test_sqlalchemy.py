
#!/usr/bin/python
# -*- coding: utf-8 -*-

from modeles import *
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json 
import jsonpickle

session = sessionmaker(bind=engine)

s = session()

#fenetre_repas = Fenetre(nom='fenetre_repas')
#zone_1_repas = Zone(nom='zone_1_repas')
#zone_1_repas.fenetre = fenetre_repas


#s.add(fenetre_repas)
fenetre = s.query(Fenetre).filter(Fenetre.nom == 'fenetre_repas').one()

for x in fenetre.zones[2].lignes:
    print(x)
    for y in x.cellules:
        print(y.contenu)

fen_dict = dict(
id = fenetre.id,
nom = fenetre.nom,
fond = fenetre.fond)

# for x in fenetre.zones:
#     fen_dict["zones"][x.id] = x.serialiser_en_json

#print(fen_dict)
test = fenetre.serialiser_en_json()

print(test)

test["nom"] = "Fenetre principale de repas WTF"

fenetre.deserialiser_de_json(test)

print(fenetre.nom)

#test = json.loads(jsonpickle.encode(fenetre))

#print(json.dumps(test, indent=4, separators=(',', ': ')))

# for attr in vars(fenetre_repas):
#     print(attr)
# print("------")
# for attr in vars(zone_1_repas):
#     print(attr)
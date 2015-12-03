#!/usr/bin/python
# -*- coding: utf-8 -*-

from modeles import *
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json 
import jsonpickle
engine = create_engine('sqlite:///src//data//database.db', encoding='utf8', convert_unicode=True)
session = sessionmaker(bind=engine)

s = session()

#fenetre_repas = Fenetre(nom='fenetre_repas')
#zone_1_repas = Zone(nom='zone_1_repas')
#zone_1_repas.fenetre = fenetre_repas

new_zone = {
            "id": "",
            "id_style": 1,
            "type": "ZoneBase"
        }
#s.add(fenetre_repas)
fenetre = s.query(Fenetre).filter(Fenetre.id == 1).one()
test = fenetre.serialiser_en_json()


# for zone in test['zones']:
#     if zone['id'] == 2:
#         zone['id'] = -2
#     print(zone['nom'])
test['zones'].append(new_zone)

# fw = open('workfile', 'w')

# fw.write(json.dumps(test, indent=4, separators=(',', ': ')))

fenetre.deserialiser_de_json(s, test)
s.commit()

# for x in fenetre.zones[2].lignes:
#     print(x)
#     for y in x.cellules:
#         print(y.contenu)


# for x in fenetre.zones:
#     fen_dict["zones"][x.id] = x.serialiser_en_json

#print(fen_dict)
#test = fenetre.serialiser_en_json()

# test['zones']['id'] = 2

# fenetre.deserialiser_de_json(s, test)

# test = fenetre.serialiser_en_json()

#print(test)
#test = json.loads(jsonpickle.encode(fenetre))
#testdata = json.dumps(test, indent=4, separators=(',', ': '))



# fr = open('workfile', 'r')
# new_data = fr.read()

# new_data_json = json.loads(new_data)

# fenetre.deserialiser_de_json(s, new_data_json)
# s.commit()
# print(fenetre.serialiser_en_json())



# for zone in new_data_json['zones']:
#     if zone["id"] == "":
#         session.add


# for attr in vars(fenetre_repas):
#     print(attr)
# print("------")
# for attr in vars(zone_1_repas):
#     print(attr)
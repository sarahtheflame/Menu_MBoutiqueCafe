#!/usr/bin/python
# -*- coding: utf-8 -*-

from modeles_temporaires import *
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json 
import jsonpickle

engine = create_engine('sqlite:///..//src//data//database.db', encoding='utf8', convert_unicode=True)
session = sessionmaker(bind=engine)

s = session()

# EXEMPLE 1 : Sérialiser une fenêtre
fenetre_repas = s.query(Fenetre).filter(Fenetre.id == 1).one()
data_fenetre_repas = fenetre_repas.serialiser_en_json()
fw = open('workfile', 'w')
fw.write(json.dumps(data_fenetre_repas, indent=4, separators=(',', ': ')))
# Résultat : Le contenu de la fenêtre se trouve dans le fichier « workfile »


# EXEMPLE 2 : Modifier le nom d'une fenêtre
fenetre_repas = s.query(Fenetre).filter(Fenetre.id == 1).one()
fenetre_repas.nom = "nouveau nom"
s.commit()
# Résultat : Le nom de la fenêtre a été modifié dans la base de données


# EXEMPLE 3 : Créer une nouvelle zone dans une fenêtre

new_zone_base = {
            "id": "",
            "id_style": 1,
            "type": "ZoneBase"
        }





#fenetre_repas = Fenetre(nom='fenetre_repas')
#zone_1_repas = Zone(nom='zone_1_repas')
#zone_1_repas.fenetre = fenetre_repas



new_zone_image = {
            "id": "",
            "image": {
                "id": 1,
                "nom": "sandwich",
                "chemin_fichier": "sandwich.jpg"
            },
            "type": "ZoneImage",
        }

new_zone_table = {
            "lignes": [
                {
                    "cellules": [
                        {
                            "id_style": 6,
                            "id": ""
                        }
                    ],
                    "id_style": 5,
                    "id": ""
                }
            ],
            "id": "",
            "type": "ZoneTable",
            "id_style": 4
        }


#fenetre_repas = s.query(Fenetre).filter(Fenetre.id == 1).one()
#fenetre_repas.id_theme = 2
# s.delete(s.query(Zone).filter(Zone.id == 3).one())

# s.commit()


# new_zone = {
#             "id": "",
#             "id_style": 1,
#             "type": "ZoneBase"
#         }

#s.add(fenetre_repas)
fenetre = s.query(Fenetre).filter(Fenetre.id == 1).one()
test = fenetre.serialiser_en_json()


for zone in test['zones']:
    print(zone['nom'])

# test['zones'].append(new_zone_base)




#fenetre.deserialiser_de_json(s, test)


theme = s.query(Theme).filter(Theme.id == 1).one()
# test2 = theme.serialiser_en_json()
# fw = open('workfile', 'w')
# fw.write(json.dumps(test2, indent=4, separators=(',', ': ')))
# theme.deserialiser_de_json(s, new_theme)
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
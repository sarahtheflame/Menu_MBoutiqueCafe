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

new_zone_base = {
            "id": "",
            "id_style": 1,
            "type": "ZoneBase"
        }
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
new_theme = {
    "tableau_sous_titre": {
        "id": 0,
        "type" : "tableau_sous_titre",
        "bordure": {
            "couleur": "#FFFFFF",
            "style": "solid",
            "taille": "0px",
            "id": 7
        }
    },
    "tableau_ligne": {
        "id": 0,
        "type" : "tableau_ligne",
        "bordure": {
            "couleur": "#FFFFFF",
            "style": "solid",
            "taille": "0px",
            "id": 7
        }
    },
    "tableau": {
        "id": 0,
        "type" : "tableau",
        "bordure": {
            "couleur": "#FFFFFF",
            "style": "solid",
            "taille": "0px",
            "id": 7
        }
    },
    "tableau_titre": {
        "id": 0,
        "type" : "tableau_titre",
        "bordure": {
            "couleur": "#FFFFFF",
            "style": "solid",
            "taille": "0px",
            "id": 7
        }
    },
    "texte": {
        "id": 0,
        "type" : "texte",
        "bordure": {
            "couleur": "#FFFFFF",
            "style": "solid",
            "taille": "0px",
            "id": 7
        }
    },
    "nom": "Nouveau theme!",
    "id": 1,
    "tableau_texte": {
        "id": 0,
        "type" : "tableau_texte",
        "bordure": {
            "couleur": "#FFFFFF",
            "style": "solid",
            "taille": "0px",
            "id": 7
        }
    },
    "titre": {
        "id": 0,
        "type" : "titre",
        "bordure": {
            "couleur": "#FFFFFF",
            "style": "solid",
            "taille": "0px",
            "id": 7
        }
    },
    "sous_titre": {
        "id": 0,
        "type" : "sous_titre",
        "bordure": {
            "couleur": "#FFFFFF",
            "style": "solid",
            "taille": "0px",
            "id": 7
        }
    }
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
#fenetre = s.query(Fenetre).filter(Fenetre.id == 1).one()
#test = fenetre.serialiser_en_json()


# for zone in test['zones']:
#     print(zone['nom'])

# test['zones'].append(new_zone_base)


# fw = open('workfile', 'w')

# fw.write(json.dumps(test, indent=4, separators=(',', ': ')))

#fenetre.deserialiser_de_json(s, test)


theme = s.query(Theme).filter(Theme.id == 1).one()
test2 = theme.serialiser_en_json()
fw = open('workfile', 'w')
fw.write(json.dumps(test2, indent=4, separators=(',', ': ')))
theme.deserialiser_de_json(s, new_theme)
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
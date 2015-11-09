
#!/usr/bin/python
# -*- coding: utf-8 -*-

from modeles import *
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

session = sessionmaker(bind=engine)

s = session()

#fenetre_repas = Fenetre(nom='fenetre_repas')
#zone_1_repas = Zone(nom='zone_1_repas')
#zone_1_repas.fenetre = fenetre_repas

theme_1 = Theme(nom='theme principal')


#s.add(fenetre_repas)
s.add(theme_1)

s.commit()

# for attr in vars(fenetre_repas):
#     print(attr)
# print("------")
# for attr in vars(zone_1_repas):
#     print(attr)
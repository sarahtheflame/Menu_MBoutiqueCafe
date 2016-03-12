#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Initialisation de l'object 'Base'. Celui-ci sera partagé avec les différents objets de ORM.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
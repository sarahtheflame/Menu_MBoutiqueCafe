#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Periode(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Représente l'ensemble des objets 'Fenetre' à
            afficher dans les écrans à une certaine heure.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            heure_debut (Time) : Heure à laquelle commence la 'Periode'.
            id_fenetre_1 (Integer) : Référence à l'identifiant d'un objet 'Fenetre'. Est associé à 
                l'attribut 'fenetre_1'.
            fenetre_1 (Relationship) : Référence à un objet 'Fenetre'. Est associé par l'attribut 
                'id_fenetre_1'.
            id_fenetre_2 (Integer) : Référence à l'identifiant d'un objet 'Fenetre'. Est associé à 
                l'attribut 'fenetre_2'.
            fenetre_2 (Relationship) : Référence à un objet 'Fenetre'. Est associé par l'attribut 
                'id_fenetre_2'.
            id_fenetre_3 (Integer) : Référence à l'identifiant d'un objet 'Fenetre'. Est associé à 
                l'attribut 'fenetre_3'.
            fenetre_3 (Relationship) : Référence à un objet 'Fenetre'. Est associé par l'attribut 
                'id_fenetre_3'.
            id_fenetre_4 (Integer) : Référence à l'identifiant d'un objet 'Fenetre'. Est associé à 
                l'attribut 'fenetre_4'.
            fenetre_4 (Relationship) : Référence à un objet 'Fenetre'. Est associé par l'attribut 
                'id_fenetre_4'.
    """
    __tablename__ = 'Periodes'
    id = Column(Integer, primary_key=True)
    heure_debut = Column(Time, unique=True)
    id_fenetre_1 = Column(
        Integer, 
        ForeignKey('Fenetres.id', onupdate='cascade', ondelete='set default'), 
        default=1
        )
    id_fenetre_2 = Column(
        Integer, 
        ForeignKey('Fenetres.id', onupdate='cascade', ondelete='set default'), 
        default=1
        )
    id_fenetre_3 = Column(
        Integer, 
        ForeignKey('Fenetres.id', onupdate='cascade', ondelete='set default'), 
        default=1
        )
    id_fenetre_4 = Column(
        Integer, 
        ForeignKey('Fenetres.id', onupdate='cascade', ondelete='set default'), 
        default=1
        )
    fenetre_1 = relationship(
        Fenetre, 
        uselist=False, 
        foreign_keys=[id_fenetre_1]
        )
    fenetre_2 = relationship(
        Fenetre, 
        uselist=False, 
        foreign_keys=[id_fenetre_2]
        )
    fenetre_3 = relationship(
        Fenetre, 
        uselist=False, 
        foreign_keys=[id_fenetre_3]
        )
    fenetre_4 = relationship(
        Fenetre, 
        uselist=False, 
        foreign_keys=[id_fenetre_4]
        )

    def serialiser_en_json(self):
        """
            Retourne un 'Dict' en format 'JSON' contenant les attributs de la classe (Nécessaire 
            puisque SQLAlchemy modifie l'architecture du '__dict__' de l'objet)
        """
        return dict(
            id = self.id,
            heure_debut = self.heure_debut,
            fenetre_1 = self.fenetre_1.serialiser_en_json(),
            fenetre_2 = self.fenetre_2.serialiser_en_json(),
            fenetre_3 = self.fenetre_3.serialiser_en_json(),
            fenetre_4 = self.fenetre_4.serialiser_en_json()
            )

    def deserialiser_de_json(self, session, data):
        """
            Assigne la valeur des attributs de l'objet à l'aide d'un 'dict' contenant les valeurs 
            à assigner.

            Arguments:
                session (Session) : Objet de la librairie 'SQLAlchemy' qui relie les objets python 
                                    à la base de données.
                data (Dict) : Dictionnaire qui contient les valeurs à assigner.
        """
        if data.get('heure_debut') != None : self.heure_debut = data['heure_debut']
        if(self.fenetre_1 != data['fenetre_1']['id']):
            self.fenetre_1 = session.query(Fenetre).filter(Fenetre.id == data['fenetre_1']['id']).one()
        if(self.fenetre_2 != data['fenetre_2']['id']):
            self.fenetre_2 = session.query(Fenetre).filter(Fenetre.id == data['fenetre_2']['id']).one()
        if(self.fenetre_3 != data['fenetre_3']['id']):
            self.fenetre_3 = session.query(Fenetre).filter(Fenetre.id == data['fenetre_3']['id']).one()
        if(self.fenetre_4 != data['fenetre_4']['id']):
            self.fenetre_4 = session.query(Fenetre).filter(Fenetre.id == data['fenetre_4']['id']).one()

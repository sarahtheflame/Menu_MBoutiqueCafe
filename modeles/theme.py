#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Définition de la classe 'Theme'. Fait partie du paquet des modèles.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""
__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'

from sqlalchemy import *
from modeles.base import Base
from modeles.style import Style
from sqlalchemy.orm import relationship, backref, sessionmaker

class Theme(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Représente un ensemble de 'Style'. Utilisé
            pour définir l'apparence d'un ou plusieurs objets 'Fenetres'.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            nom (String) : Nom de l'objet 'Theme'.
            id_titre (Integer) : Référence à l'identifiant d'un objet 'Style'. Est associé à
                l'attribut 'titre'.
            id_sous_titre (Integer) : Référence à l'identifiant d'un objet 'Style'. Est associé à
                 l'attribut 'sous_titre'.
            id_texte (Integer) : Référence à l'identifiant d'un objet 'Style'. Est associé à
                l'attribut 'texte'.
            id_tableau (Integer) : Référence à l'identifiant d'un objet 'Style'. Est associé à
                 l'attribut 'tableau'.
            id_tableau_ligne (Integer) : Référence à l'identifiant d'un objet 'Style'. Est associé
                 à l'attribut 'tableau_ligne'.
            id_tableau_titre (Integer) : Référence à l'identifiant d'un objet 'Style'. Est associé à
                 l'attribut 'tableau_titre'.
            id_tableau_sous_titre (Integer) : Référence à l'identifiant d'un objet 'Style'. Est
                associé à l'attribut 'tableau_sous_titre'.
            id_tableau_texte (Integer) : Référence à l'identifiant d'un objet 'Style'. Est associé à
                l'attribut 'tableau_texte'.
            titre (Relationship) : Référence à un objet 'Style'. Est associé par l'attribut
                'id_titre'.
            sous_titre (Relationship) : Référence à un objet 'Style'. Est associé par l'attribut
                'id_sous_titre'.
            texte (Relationship) : Référence à un objet 'Style'. Est associé par l'attribut
                'id_texte'.
            tableau (Relationship) : Référence à un objet 'Style'. Est associé par l'attribut
                'id_tableau'.
            tableau_ligne (Relationship) : Référence à un objet 'Style'. Est associé par l'attribut
                'id_tableau_ligne'.
            tableau_titre (Relationship) : Référence à un objet 'Style'. Est associé par l'attribut
                'id_tableau_titre'.
            tableau_sous_titre (Relationship) : Référence à un objet 'Style'. Est associé par
                l'attribut 'id_tableau_sous_titre'.
            tableau_texte (Relationship) : Référence à un objet 'Style'. Est associé par l'attribut
                'id_tableau_texte'.
            ** fenetres (List) : Liste d'objets 'Fenetre' (créée par la fonction 'backref' lancée
                par la classe 'Fenetre').
    """
    __tablename__ = 'Themes'
    id = Column(
        Integer, 
        primary_key=True
        )
    nom = Column(
        String(250),
        nullable=False
        )
    id_titre = Column(
        Integer, 
        ForeignKey('Styles.id', onupdate="cascade", ondelete="cascade"),
        nullable=False
        )
    id_sous_titre = Column(
        Integer, 
        ForeignKey('Styles.id', onupdate="cascade", ondelete="cascade"),
        nullable=False
        )
    id_texte = Column(
        Integer, 
        ForeignKey('Styles.id', onupdate="cascade", ondelete="cascade"),
        nullable=False
        )
    id_tableau = Column(
        Integer, 
        ForeignKey('Styles.id', onupdate="cascade", ondelete="cascade"),
        nullable=False
        )
    id_tableau_ligne = Column(
        Integer, 
        ForeignKey('Styles.id', onupdate="cascade", ondelete="cascade"),
        nullable=False
        )
    id_tableau_titre = Column(
        Integer, 
        ForeignKey('Styles.id', onupdate="cascade", ondelete="cascade"),
        nullable=False
        )
    id_tableau_sous_titre = Column(
        Integer, 
        ForeignKey('Styles.id', onupdate="cascade", ondelete="cascade"),
        nullable=False
        )
    id_tableau_texte = Column(
        Integer, 
        ForeignKey('Styles.id', onupdate="cascade", ondelete="cascade"),
        nullable=False
        )

    titre = relationship(
        "Style", 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_titre]
        )
    sous_titre = relationship(
        "Style", 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_sous_titre]
        )
    texte = relationship(
        "Style", 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_texte]
        )
    tableau = relationship(
        "Style", 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_tableau]
        )
    tableau_ligne = relationship(
        "Style", 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_tableau_ligne]
        )
    tableau_titre = relationship(
        "Style", 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_tableau_titre]
        )
    tableau_sous_titre = relationship(
        "Style", 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_tableau_sous_titre]
        )
    tableau_texte = relationship(
        "Style", 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_tableau_texte]
        )

    def serialiser_en_json(self):
        """
            Retourne un 'Dict' en format 'JSON' contenant les attributs de la classe (Nécessaire 
            puisque SQLAlchemy modifie l'architecture du '__dict__' de l'objet)
        """
        return dict(
            id = self.id,
            nom = self.nom,
            titre = self.titre.serialiser_en_json(),
            sous_titre = self.sous_titre.serialiser_en_json(),
            texte = self.texte.serialiser_en_json(),
            tableau = self.tableau.serialiser_en_json(),
            tableau_ligne = self.tableau_ligne.serialiser_en_json(),
            tableau_titre = self.tableau_titre.serialiser_en_json(),
            tableau_sous_titre = self.tableau_sous_titre.serialiser_en_json(),
            tableau_texte = self.tableau_texte.serialiser_en_json()
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
        #================================ à revérifier!!! ===========================================
        if data.get('nom') != None : self.nom = data['nom']
        if data.get('titre') == None:
            self.titre = Style(bordure=Bordure())
            # self.titre.deserialiser_de_json(session, data['titre'])
            session.add(self.titre)
        elif data['titre']['id'] > 0:
            self.titre.deserialiser_de_json(session, data['titre'])
        else:
            print("Identifiant de style incorrect pour" + self.nom)
            
        if data.get('sous_titre') == None:
            self.sous_titre = Style(bordure=Bordure())
            # self.sous_titre.deserialiser_de_json(session, data['sous_titre'])
            session.add(self.sous_titre)
        elif data['sous_titre']['id'] > 0:
            self.sous_titre.deserialiser_de_json(session, data['sous_titre'])
        else:
            print("Identifiant de style incorrect pour" + self.nom)
            
        if data.get('texte') == None:
            self.texte = Style(bordure=Bordure())
            # self.texte.deserialiser_de_json(session, data['texte'])
            session.add(self.texte)
        elif data['texte']['id'] > 0:
            self.texte.deserialiser_de_json(session, data['texte'])
        else:
            print("Identifiant de style incorrect pour" + self.nom)
            
        if data.get('tableau') == None:
            self.tableau = Style(bordure=Bordure())
            # self.tableau.deserialiser_de_json(session, data['tableau'])
            session.add(self.tableau)
        elif data['tableau']['id'] > 0:
            self.tableau.deserialiser_de_json(session, data['tableau'])
        else:
            print("Identifiant de style incorrect pour" + self.nom)
            
        if data.get('tableau_ligne') == None:
            self.tableau_ligne = Style(bordure=Bordure())
            # self.tableau_ligne.deserialiser_de_json(session, data['tableau_ligne'])
            session.add(self.tableau_ligne)
        elif data['tableau_ligne']['id'] > 0:
            self.tableau_ligne.deserialiser_de_json(session, data['tableau_ligne'])
        else:
            print("Identifiant de style incorrect pour" + self.nom)
            
        if data.get('tableau_titre') == None:
            self.tableau_titre = Style(bordure=Bordure())
            # self.tableau_titre.deserialiser_de_json(session, data['tableau_titre'])
            session.add(self.tableau_titre)
        elif data['tableau_titre']['id'] > 0:
            self.tableau_titre.deserialiser_de_json(session, data['tableau_titre'])
        else:
            print("Identifiant de style incorrect pour" + self.nom)
            
        if data.get('tableau_sous_titre') == None:
            self.tableau_sous_titre = Style(bordure=Bordure())
            # self.tableau_sous_titre.deserialiser_de_json(session, data['tableau_sous_titre'])
            session.add(self.tableau_sous_titre)
        elif data['tableau_sous_titre']['id'] > 0:
            self.tableau_sous_titre.deserialiser_de_json(session, data['tableau_sous_titre'])
        else:
            print("Identifiant de style incorrect pour" + self.nom)

        if data.get('tableau_texte') == None:
            self.tableau_texte = Style(bordure=Bordure())
            # self.tableau_texte.deserialiser_de_json(session, data['tableau_texte'])
            session.add(self.tableau_texte)
        elif data['tableau_texte']['id'] > 0:
            self.tableau_texte.deserialiser_de_json(session, data['tableau_texte'])
        else:
            print("Identifiant de style incorrect pour" + self.nom)


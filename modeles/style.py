#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Définition de la classe 'Style'. Fait partie du paquet des modèles.
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""

from bordure import *
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Style(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Représente un ensemble de 'Style'. Utilisé
            pour définir l'apparence d'un ou plusieurs objets 'Fenetres'.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            police (String) : Attribut CSS de la police d'écriture (ex: "'KaushanScript', cursive").
            couleur (String) : Attribut CSS de la couleur du texte (ex: "#FFFFFF").
            taille (String) : Attribut CSS de la taille du texte (ex: "4vw").
            couleur_fond (String) : Attribut CSS de la couleur et de l'opacité du fond 
                (ex: "rgba(0, 0, 0, 0.8)").
            gras (String) : Attribut CSS indiquant si le texte est en gras 
                (valeurs : normal|bold|bolder|lighter|'integer'|initial|inherit).
            italique (String) : Attribut CSS indiquant si le texte est en italique 
                (valeurs : normal|italic|oblique|initial|inherit).
            soulignement (String) : Attribut CSS indiquant si le texte est souligné 
                (valeurs : none|underline|overline|line-through|initial|inherit).
            type (String) : Sert à déterminer à quel attribut du theme l'objet 'Style' est associé 
                (Voir 'deserialiser_de_json()' de 'Theme'.
            id_bordure (Integer) : Référence à l'identifiant d'un objet 'Bordure'. Est associé à
                l'attribut 'bordure'.
            bordure (Relationship) : Référence à un objet 'Bordure'. Est associé par l'attribut
                'id_bordure'.
    """
    __tablename__ = 'Styles'
    id = Column(Integer, primary_key=True)
    police = Column(String(250), default='\'Oswald\', sans-serif')
    couleur = Column(String(250), default='#000000')
    taille = Column(Integer, default='1.5vw')
    couleur_fond = Column(String(250), default='rgba(0, 0, 0, 0.8)')
    gras = Column(String(250), default='normal')
    italique = Column(String(250), default='normal')
    soulignement = Column(String(250), default='none')
    type = Column(String(250), default='texte')
    id_bordure = Column(
        Integer, 
        ForeignKey('Bordures.id', onupdate="cascade", ondelete="cascade"),
        nullable=False
        )
    bordure = relationship(
        Bordure,
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_bordure]
        )

    def serialiser_en_json(self):
        """
            Retourne un 'Dict' en format 'JSON' contenant les attributs de la classe (Nécessaire 
            puisque SQLAlchemy modifie l'architecture du '__dict__' de l'objet)
        """
        return dict(
            id = self.id,
            police = self.police,
            couleur = self.couleur,
            taille = self.taille,
            couleur_fond = self.couleur_fond,
            opacite_fond = self.opacite_fond,
            gras = self.gras,
            italique = self.italique,
            soulignement = self.soulignement,
            bordure = self.bordure.serialiser_en_json()
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
        if data.get('police') != None : self.police = data['police']
        if data.get('couleur') != None : self.couleur = data['couleur']
        if data.get('taille') != None : self.taille = data['taille']
        if data.get('couleur_fond') != None : self.couleur_fond = data['couleur_fond']
        if data.get('opacite_fond') != None : self.opacite_fond = data['opacite_fond']
        if data.get('gras') != None : self.gras = data['gras']
        if data.get('italique') != None : self.italique = data['italique']
        if data.get('soulignement') != None : self.soulignement = data['soulignement']
        if (data['bordure']['id'] == 0):
            nouvelle_bordure = Bordure()
            nouvelle_bordure.deserialiser_de_json(session, data['bordure'])
            session.add(nouvelle_bordure)
            self.bordure = nouvelle_bordure
        elif (data['bordure']['id'] > 0):
            self.bordure.deserialiser_de_json(session, data['bordure'])
        else:  
            print('Impossible de déserialiser la bordure')
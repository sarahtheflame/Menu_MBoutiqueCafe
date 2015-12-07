#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class Media(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Est une classe abstraite qui contient les informations de base communes à tous les types de médias.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            nom (String) : Nom de la zone.
            chemin_fichier (String) : Chemin de fichier (relatif au serveur) qui pointe vers la ressource (ex: /src/images/exemple.png).
            type (String) : Type polymorphique du média (voir l'attribut '__mapper_args___').
            __mapper_args__ (Dictionary) : Contient les options qui configurent le polymorphisme de la classe.
    """
    __tablename__ = 'Medias'
    id = Column(Integer, primary_key=True)
    nom = Column(String, default="Media sans nom")
    chemin_fichier = Column(String)
    type = Column(String)

    def serialiser_en_json(self):
        return dict(
            id = self.id,
            nom = self.nom,
            chemin_fichier = self.chemin_fichier)

    def deserialiser_de_json(self, session, data):
        if data.get('nom') != None : self.nom = data['nom']
        if data.get('chemin_fichier') != None : self.chemin_fichier = data['chemin_fichier']
        
    __mapper_args__ = {
        'polymorphic_identity':'Media',
        'polymorphic_on':type
    }

class Image(Media):
    """
        Description: 
            Hérite de la classe 'Media'. Permet de différencier un média de type 'Image' des autres types.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Référence à l'identifiant unique d'un 'Media'.
            __mapper_args__ (Dictionary) : Contient les options qui configurent le polymorphisme de la classe.
    """
    __tablename__ = 'Images'
    id = Column(Integer, ForeignKey('Medias.id', onupdate="cascade", ondelete="cascade"), primary_key=True)
        
    __mapper_args__ = {
        'polymorphic_identity':'Image'
    }

class Video(Media):
    """
        Description: 
            Hérite de la classe 'Media'. Permet de différencier un média de type 'Video' des autres types.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Référence à l'identifiant unique d'un 'Media'.
            __mapper_args__ (Dictionary) : Contient les options qui configurent le polymorphisme de la classe.
    """
    __tablename__ = 'Videos'
    id = Column(Integer, ForeignKey('Medias.id', onupdate="cascade", ondelete="cascade"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'Video'
    }

class Bordure(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Représente des attributs CSS utilisés pour définir l'apparence de la bordure d'un objet 'Style'.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            taille (String) : Attribut CSS de la taille (ex: "1px").
            style (String) : Attribut CSS du style (valeurs: "none|hidden|dotted|dashed|solid|double|groove|ridge|inset|outset|initial|inherit").
            couleur (String) : Attribut CSS de la couleur et de l'opacité (ex: "rgba(0, 0, 0, 0.8)").
    """
    __tablename__ = 'Bordures'
    id = Column(Integer, primary_key=True)
    taille = Column(String(250), default='0px')
    style = Column(String(250), default='solid')
    couleur = Column(String(250), default='#000000')

    def serialiser_en_json(self):
        return dict(
            id = self.id,
            taille = self.taille,
            style = self.style
            couleur = self.couleur,
            )

    def deserialiser_de_json(self, session, data):
        if data.get('taille') != None : self.taille = data['taille']
        if data.get('style') != None : self.style = data['style']
        if data.get('couleur') != None : self.couleur = data['couleur']

class Style(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Représente un ensemble de 'Style'. Utilisé pour définir l'apparence d'un ou plusieurs objets 'Fenetres'.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            police (String) : Attribut CSS de la police d'écriture (ex: "'KaushanScript', cursive").
            couleur (String) : Attribut CSS de la couleur du texte (ex: "#FFFFFF").
            taille (String) : Attribut CSS de la taille du texte (ex: "4vw").
            fond (String) : Attribut CSS de la couleur et de l'opacité du fond (ex: "rgba(0, 0, 0, 0.8)").
            gras (String) : Attribut CSS indiquant si le texte est en gras (valeurs : normal|bold|bolder|lighter|'integer'|initial|inherit).
            italique (String) : Attribut CSS indiquant si le texte est en italique (valeurs : normal|italic|oblique|initial|inherit).
            soulignement (String) : Attribut CSS indiquant si le texte est souligné (valeurs : none|underline|overline|line-through|initial|inherit).
            type (String) : Sert à déterminer à quel attribut du theme l'objet 'Style' est associé (Voir 'deserialiser_de_json()' de 'Theme'.
            id_bordure (Integer) : Référence à l'identifiant d'un objet 'Bordure'. Est associé à l'attribut 'bordure'.
            bordure (Relationship) : Référence à un objet 'Bordure'. Est associé par l'attribut 'id_bordure'.
    """
    __tablename__ = 'Styles'
    id = Column(Integer, primary_key=True)
    police = Column(String(250), default='\'Oswald\', sans-serif')
    couleur = Column(String(250), default='#000000')
    taille = Column(Integer, default='1.5vw')
    couleur_fond = Column(String(250), default='#FFFFFF')
    opacite_fond = Column(String, default='0')
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
            

class Theme(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Représente un ensemble de 'Style'. Utilisé pour définir l'apparence d'un ou plusieurs objets 'Fenetres'.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            nom (String) : Nom de l'objet 'Theme'.
            id_titre (Integer) : Référence à l'identifiant d'un objet 'Style'. Est associé à l'attribut 'titre'.
            id_sous_titre (Integer) : Référence à l'identifiant d'un objet 'Style'. Est associé à l'attribut 'sous_titre'.
            id_texte (Integer) : Référence à l'identifiant d'un objet 'Style'. Est associé à l'attribut 'texte'.
            id_tableau (Integer) : Référence à l'identifiant d'un objet 'Style'. Est associé à l'attribut 'tableau'.
            id_tableau_ligne (Integer) : Référence à l'identifiant d'un objet 'Style'. Est associé à l'attribut 'tableau_ligne'.
            id_tableau_titre (Integer) : Référence à l'identifiant d'un objet 'Style'. Est associé à l'attribut 'tableau_titre'.
            id_tableau_sous_titre (Integer) : Référence à l'identifiant d'un objet 'Style'. Est associé à l'attribut 'tableau_sous_titre'.
            id_tableau_texte (Integer) : Référence à l'identifiant d'un objet 'Style'. Est associé à l'attribut 'tableau_texte'.
            titre (Relationship) : Référence à un objet 'Style'. Est associé par l'attribut 'id_titre'.
            sous_titre (Relationship) : Référence à un objet 'Style'. Est associé par l'attribut 'id_sous_titre'.
            texte (Relationship) : Référence à un objet 'Style'. Est associé par l'attribut 'id_texte'.
            tableau (Relationship) : Référence à un objet 'Style'. Est associé par l'attribut 'id_tableau'.
            tableau_ligne (Relationship) : Référence à un objet 'Style'. Est associé par l'attribut 'id_tableau_ligne'.
            tableau_titre (Relationship) : Référence à un objet 'Style'. Est associé par l'attribut 'id_tableau_titre'.
            tableau_sous_titre (Relationship) : Référence à un objet 'Style'. Est associé par l'attribut 'id_tableau_sous_titre'.
            tableau_texte (Relationship) : Référence à un objet 'Style'. Est associé par l'attribut 'id_tableau_texte'.
            ** fenetres (List) : Liste d'objets 'Fenetre' (créée par la fonction 'backref' lancée par la classe 'Fenetre').
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
        Style, 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_titre]
        )
    sous_titre = relationship(
        Style, 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_sous_titre]
        )
    texte = relationship(
        Style, 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_texte]
        )
    tableau = relationship(
        Style, 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_tableau]
        )
    tableau_ligne = relationship(
        Style, 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_tableau_ligne]
        )
    tableau_titre = relationship(
        Style, 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_tableau_titre]
        )
    tableau_sous_titre = relationship(
        Style, 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_tableau_sous_titre]
        )
    tableau_texte = relationship(
        Style, 
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_tableau_texte]
        )

    def serialiser_en_json(self):
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
        if data.get('nom') != None : self.nom = data['nom']
        # On ne peut supprimer un style lors de la déserialisation d'un theme??
        for style in data:
            print(data[style])
            if isinstance(data[style], dict):
                print("in")
                if (data[style]['id'] == 0):
                    print('Nouveau style')
                    nouveau_style = Style(bordure=Bordure())
                    nouveau_style.deserialiser_de_json(session, data[style])
                    session.add(nouveau_style)
                    if data[style]['type'] == 'titre':
                        self.titre = nouveau_style
                    elif data[style]['type'] == 'sous_titre':
                        self.sous_titre = nouveau_style
                    elif data[style]['type'] == 'texte':
                        self.texte = nouveau_style
                    elif data[style]['type'] == 'tableau':
                        self.tableau = nouveau_style
                    elif data[style]['type'] == 'tableau_titre': 
                        self.tableau_titre = nouveau_style
                    elif data[style]['type'] == 'tableau_sous_titre': 
                        self.tableau_sous_titre = nouveau_style
                    elif data[style]['type'] == 'tableau_ligne':
                        self.tableau_ligne = nouveau_style
                    elif data[style]['type'] == 'tableau_texte':
                        self.tableau_texte = nouveau_style
                    else:
                        print("Type de style invalide")
                elif (data[style]['id'] > 0):
                    self.titre.deserialiser_de_json(session, data[style])
                else:
                    print('Impossible de déserialiser le style \'titre\'')


class Fenetre(Base):
    """
        Description: 
            Représente l'ensemble des informations qui seront utilisées pour générer une page du système d'affichage.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            nom (String) : Nom de la fenêtre.
            couleur_fond (String) : Code de couleur hexadécimal représentant la couleur utilisée pour le fond.
            id_image_fond (Integer) : Référence à l'identifiant d'un objet 'Image'. Est associé à l'attribut 'image_fond'.
            id_theme (Integer) : Référence à l'identifiant d'un objet 'Theme'. Est associé à l'attribut 'theme'.
            image_fond (Relationship) : Référence à l'objet 'Image' utilisé pour le fond. 
            theme (Relationship) : Référence à l'objet 'Theme' associé.
            ** zones (List) : Liste d'objets 'Zone' (créée par la fonction 'backref' lancée par la classe 'Zone').
    """
    __tablename__ = 'Fenetres'
    id = Column(Integer, primary_key=True)
    nom = Column(String, default="Fenetre sans nom")
    couleur_fond = Column(String, default="#FFFFFF")
    id_image_fond = Column(Integer, ForeignKey('Images.id', onupdate="cascade", ondelete="set default"), default=1)    # DEFAULT VALIDE??
    id_theme = Column(Integer, ForeignKey('Themes.id', onupdate="cascade", ondelete="set default"), default=1)  # DEFAULT VALIDE??
    image_fond = relationship(
        Image, 
        foreign_keys=[id_image_fond])
    theme = relationship(
        Theme, 
        backref=backref(
            'fenetres', 
            uselist=True),
        foreign_keys=[id_theme])

    def serialiser_en_json(self):
        zones_data = []
        data = dict(
            id = self.id,
            nom = self.nom,
            couleur_fond = self.couleur_fond,
            image_fond = self.image_fond.serialiser_en_json(),
            theme = self.theme.serialiser_en_json()
            )
        for zone in self.zones:
            zones_data.append(zone.serialiser_en_json())
        data['zones'] = zones_data
        return data

    def deserialiser_de_json(self, session, data):
        if data.get('nom') != None : self.nom = data['nom']
        if data.get('couleur_fond') != None : self.couleur_fond = data['couleur_fond']
        if (self.id_theme != data['theme']['id']):
            self.theme = session.query(Theme).filter(Theme.id == data['theme']['id']).one()
        if (self.id_image_fond != data['image_fond']['id']):
            self.image_fond = session.query(Image).filter(Image.id == data['image_fond']['id']).one()
        for zone in data['zones']:
            if zone['id'] == 0:
                if zone['type'] == 'ZoneBase':
                    nouvelle_zone = ZoneBase(fenetre=self)
                    nouvelle_zone.deserialiser_de_json(session, zone)
                    session.add(nouvelle_zone)
                elif zone['type'] == 'ZoneTable':
                    nouvelle_zone = ZoneTable(fenetre=self)
                    nouvelle_zone.deserialiser_de_json(session, zone)
                    session.add(nouvelle_zone)
                elif zone['type'] == 'ZoneImage':
                    nouvelle_zone = ZoneImage(fenetre=self)
                    nouvelle_zone.deserialiser_de_json(session, zone)
                    session.add(nouvelle_zone)
                elif zone['type'] == 'ZoneVideo':
                    nouvelle_zone = ZoneVideo(fenetre=self)
                    nouvelle_zone.deserialiser_de_json(session, zone)
                    session.add(nouvelle_zone)
                else:
                    print("Type de zone inexistante!") # IMPLÉMENTER UNE ERREUR CORRECTE
            elif zone['id'] > 0:
                session.query(Zone).filter(Zone.id == zone['id']).one().deserialiser_de_json(session, zone)
            elif zone['id'] < 0:
                session.delete(session.query(Zone).filter(Zone.id == -zone['id']).one())
            else:
                print('Impossible de déserialiser la zone')

class Periode(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Représente l'ensemble des objets 'Fenetre' à afficher dans les écrans à une certaine heure.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            heure_debut (Time) : Heure à laquelle commence la 'Periode'.
            id_fenetre_1 (Integer) : Référence à l'identifiant d'un objet 'Fenetre'. Est associé à l'attribut 'fenetre_1'.
            fenetre_1 (Relationship) : Référence à un objet 'Fenetre'. Est associé par l'attribut 'id_fenetre_1'.
            id_fenetre_2 (Integer) : Référence à l'identifiant d'un objet 'Fenetre'. Est associé à l'attribut 'fenetre_2'.
            fenetre_2 (Relationship) : Référence à un objet 'Fenetre'. Est associé par l'attribut 'id_fenetre_2'.
            id_fenetre_3 (Integer) : Référence à l'identifiant d'un objet 'Fenetre'. Est associé à l'attribut 'fenetre_3'.
            fenetre_3 (Relationship) : Référence à un objet 'Fenetre'. Est associé par l'attribut 'id_fenetre_3'.
            id_fenetre_4 (Integer) : Référence à l'identifiant d'un objet 'Fenetre'. Est associé à l'attribut 'fenetre_4'.
            fenetre_4 (Relationship) : Référence à un objet 'Fenetre'. Est associé par l'attribut 'id_fenetre_4'.
    """
    __tablename__ = 'Periodes'
    id = Column(Integer, primary_key=True)
    heure_debut = Column(Time, unique=True)
    id_fenetre_1 = Column(Integer, ForeignKey('Fenetres.id', onupdate='cascade', ondelete='set default'), default=1)
    id_fenetre_2 = Column(Integer, ForeignKey('Fenetres.id', onupdate='cascade', ondelete='set default'), default=1)
    id_fenetre_3 = Column(Integer, ForeignKey('Fenetres.id', onupdate='cascade', ondelete='set default'), default=1)
    id_fenetre_4 = Column(Integer, ForeignKey('Fenetres.id', onupdate='cascade', ondelete='set default'), default=1)
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
        return dict(
            id = self.id,
            heure_debut = self.heure_debut,
            fenetre_1 = self.fenetre_1.serialiser_en_json(),
            fenetre_2 = self.fenetre_2.serialiser_en_json(),
            fenetre_3 = self.fenetre_3.serialiser_en_json(),
            fenetre_4 = self.fenetre_4.serialiser_en_json()
            )

    def deserialiser_de_json(self, session, data):
        if data.get('heure_debut') != None : self.heure_debut = data['heure_debut']
        if(self.fenetre_1 != data['fenetre_1']['id']):
            self.fenetre_1 = session.query(Fenetre).filter(Fenetre.id == data['fenetre_1']['id']).one()
        if(self.fenetre_2 != data['fenetre_2']['id']):
            self.fenetre_2 = session.query(Fenetre).filter(Fenetre.id == data['fenetre_2']['id']).one()
        if(self.fenetre_3 != data['fenetre_3']['id']):
            self.fenetre_3 = session.query(Fenetre).filter(Fenetre.id == data['fenetre_3']['id']).one()
        if(self.fenetre_4 != data['fenetre_4']['id']):
            self.fenetre_4 = session.query(Fenetre).filter(Fenetre.id == data['fenetre_4']['id']).one()

class Zone(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Est une classe abstraite qui contient les informations de base communes à tous les types de zones.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            nom (String) : Nom de la zone.
            position_x (String) : Attribut CSS de la position horizontale de la zone (ex: "10%"). 
            position_y (String) : Attribut CSS de la position verticale de la zone (ex: "10%"). 
            largeur (String) : Attribut CSS de la largeur de la zone (ex: "10%").
            hauteur (String) : Attribut CSS de la hauteur de la zone (ex: "10%").
            type (String) : Type polymorphique de la zone (voir l'attribut '__mapper_args___').
            id_fenetre (Integer) : Référence à l'identifiant d'un objet 'Fenetre'.
            fenetre (Relationship) : Référence à l'objet 'Fenetre' associé. La fonction 'backref' crée une liste d'objets 'Zone' dans cet objet.
            __mapper_args__ (Dictionary) : Contient les options qui configurent le polymorphisme de la classe.
    """
    __tablename__ = 'Zones'
    id = Column(Integer, primary_key=True)
    nom = Column(String, default='Zone sans nom')
    position_x = Column(String, default='0%')
    position_y = Column(String, default='0%')
    largeur = Column(String, default='0%')
    hauteur = Column(String, default='0%')
    type = Column(String(50))
    id_fenetre = Column(Integer, ForeignKey('Fenetres.id', onupdate='cascade', ondelete='cascade'))
    fenetre = relationship(
        Fenetre, 
        backref=backref(
            'zones', 
            uselist=True, 
            cascade='delete,all')
        )

    __mapper_args__ = {
        'polymorphic_identity':'Zone',
        'polymorphic_on':type
    }

class ZoneBase(Zone):
    """
        Description: 
            La classe 'ZoneBase' hérite de la classe 'Zone'. Sert à représenter un rectangle contenant ou non du texte.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Référence à l'identifiant unique d'une 'Zone'.
            contenu (String) : Texte contenu dans la zone. 
            id_style (Integer) : Référence à l'identifiant d'un objet 'Style'.
            style (Relationship) : Référence à l'objet 'Style' associé.
            __mapper_args__ (Dictionary) : Contient les options qui configurent le polymorphisme de la classe.
    """
    __tablename__ = 'ZonesBase'
    id = Column(Integer, ForeignKey('Zones.id', onupdate='cascade', ondelete='cascade'), primary_key=True)
    contenu = Column(String, default="")
    id_style = Column(Integer, ForeignKey('Styles.id', onupdate='cascade', ondelete='set default'), default=3)
    style = relationship(
        Style,
        uselist=False,
        foreign_keys=[id_style]
    )

    def serialiser_en_json(self):
        """
            Retourne un 'Dict' en format 'JSON' contenant les attributs de la classe (Nécessaire 
            puisque SQLAlchemy modifie l'architecture du '__dict__' de l'objet)
        """
        return dict(
            id = self.id,
            contenu = self.contenu,
            nom = self.nom,
            position_x = self.position_x,
            position_y = self.position_y,
            largeur = self.largeur,
            hauteur = self.hauteur,
            type = self.type,
            id_style = self.id_style
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
        if data.get('contenu') != None : self.contenu = data['contenu']
        if data.get('nom') != None : self.nom = data['nom']
        if data.get('position_x') != None : self.position_x = data['position_x']
        if data.get('position_y') != None : self.position_y = data['position_y']
        if data.get('largeur') != None : self.largeur = data['largeur']
        if data.get('hauteur') != None : self.hauteur = data['hauteur']
        if (self.id_style != data['id_style']): # Ne peut être null...
            self.style = session.query(Style).filter(Style.id == data['id_style']).one()

    __mapper_args__ = {
        'polymorphic_identity':'ZoneBase',
    }

class ZoneImage(Zone):
    """
        Description: 
            La classe 'ZoneImage' hérite de la classe 'Zone'. Contient une 'Image'.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Référence à l'identifiant unique d'une 'Zone'.
            id_image (Integer) : Référence à l'identifiant d'un objet 'Image'.
            image (Relationship) : Référence à l'objet 'Image' associé.
            __mapper_args__ (Dictionary) : Contient les options qui configurent le polymorphisme de la classe.
    """
    __tablename__ = 'ZonesImage'
    id = Column(Integer, ForeignKey('Zones.id', onupdate='cascade', ondelete='cascade'), primary_key=True)
    id_image = Column(Integer, ForeignKey('Images.id', onupdate='cascade', ondelete='cascade')) # NULLABLE?
    image = relationship(
        Image, 
        backref=backref(
            'zones_images', 
            uselist=True, 
            cascade='delete,all'),
        foreign_keys=[id_image]
        )

    __mapper_args__ = {
        'polymorphic_identity':'ZoneImage',
    }

    def serialiser_en_json(self):
        return dict(
            id = self.id,
            nom = self.nom,
            position_x = self.position_x,
            position_y = self.position_y,
            largeur = self.largeur,
            hauteur = self.hauteur,
            type = self.type,
            image = self.image.serialiser_en_json()
            )

    def deserialiser_de_json(self, session, data):
        if (self.id_image != data['image']['id']):
            self.image = session.query(Image).filter(Image.id == data['image']['id']).one()
        if data.get('nom') != None : self.nom = data['nom']
        if data.get('position_x') != None : self.position_x = data['position_x']
        if data.get('position_y') != None : self.position_y = data['position_y']
        if data.get('largeur') != None : self.largeur = data['largeur']
        if data.get('hauteur') != None : self.hauteur = data['hauteur']

class ZoneVideo(Zone):
    """
        Description: 
            Hérite de la classe 'Zone'. Contient un 'Video'.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Référence à l'identifiant unique d'une 'Zone'.
            id_video (Integer) : Référence à l'identifiant d'un objet 'Video'
            video (Relationship) : Référence à l'objet 'Video' associé. Dans cet objet, la fonction 'backref' crée une liste des 'ZoneVideo' qui l'utilisent.
            __mapper_args__ (Dictionary) : Contient les options qui configurent le polymorphisme de la classe.
    """
    __tablename__ = 'ZonesVideo'
    id = Column(Integer, ForeignKey('Zones.id', onupdate='cascade', ondelete='cascade'), primary_key=True)
    id_video = Column(Integer, ForeignKey('Videos.id', onupdate='cascade', ondelete='cascade')) # NULLABLE?
    video = relationship(
        Video, 
        backref=backref(
            'zones_videos', 
            uselist=True,
            cascade='delete,all'),
        foreign_keys=[id_video]
        )

    __mapper_args__ = {
        'polymorphic_identity':'ZoneVideo',
    }

    def serialiser_en_json(self):
        return dict(
            id = self.id,
            nom = self.nom,
            position_x = self.position_x,
            position_y = self.position_y,
            largeur = self.largeur,
            hauteur = self.hauteur,
            type = self.type,
            video = self.video.serialiser_en_json()
            )

    def deserialiser_de_json(self, session, data):
        if (self.id_video != data['video']['id']):
            self.video = session.query(Video).filter(Video.id == data['video']['id']).one()
        if data.get('nom') != None : self.nom = data['nom']
        if data.get('position_x') != None : self.position_x = data['position_x']
        if data.get('position_y') != None : self.position_y = data['position_y']
        if data.get('largeur') != None : self.largeur = data['largeur']
        if data.get('hauteur') != None : self.hauteur = data['hauteur']

class ZoneTable(Zone):
    """
        Description: 
            Hérite de la classe 'Zone'. Contient des lignes, qui elles contiennent des cellules, ce qui constitue une table.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Référence à l'identifiant unique d'une 'Zone'.
            id_style (Integer) : Référence à l'identifiant d'un objet 'Style'.
            style (Relationship) : Référence à l'objet 'Style' associé.
            __mapper_args__ (Dictionary) : Contient les options qui configurent le polymorphisme de la classe.
            ** lignes (List) : Liste d'objets 'Ligne' (créée par la fonction 'backref' lancée par la classe 'Ligne').
    """
    __tablename__ = 'ZonesTable'
    id = Column(Integer, ForeignKey('Zones.id', onupdate='cascade', ondelete='cascade'), primary_key=True)
    id_style = Column(Integer, ForeignKey('Styles.id', onupdate='cascade', ondelete='set default'), default=4)
    style = relationship(
        Style,
        uselist=False,
        foreign_keys=[id_style]
    )

    __mapper_args__ = {'polymorphic_identity':'ZoneTable'}

    def serialiser_en_json(self):
        lignes_data = []
        data = dict(
            id = self.id,
            nom = self.nom,
            position_x = self.position_x,
            position_y = self.position_y,
            largeur = self.largeur,
            hauteur = self.hauteur,
            type = self.type,
            id_style = self.id_style
            )
        for ligne in self.lignes:
            lignes_data.append(ligne.serialiser_en_json())
        data['lignes'] = lignes_data
        return data

    def deserialiser_de_json(self, session, data):
        if data.get('nom') != None : self.nom = data['nom']
        if data.get('position_x') != None : self.position_x = data['position_x']
        if data.get('position_y') != None : self.position_y = data['position_y']
        if data.get('largeur') != None : self.largeur = data['largeur']
        if data.get('hauteur') != None : self.hauteur = data['hauteur']
        if self.id_style != data['id_style']:
            self.style = session.query(Style).filter(Style.id == data['id_style']).one()
        for ligne in data['lignes']:
            if (ligne['id'] == 0):
                print('Nouvelle ligne')
                nouvelle_ligne = Ligne(zone_table=self)
                nouvelle_ligne.deserialiser_de_json(session, ligne)
                session.add(nouvelle_ligne)
            elif ligne['id'] > 0:
                session.query(Ligne).filter(Ligne.id == ligne['id']).one().deserialiser_de_json(session, ligne)
            elif ligne['id'] < 0:
                session.delete(session.query(Ligne).filter(Ligne.id == -ligne['id']).one())
            else:
                print('Impossible de déserialiser la ligne')

class Ligne(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Correspond à une ligne d'une 'ZoneTable'.
        
        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            id_zone_table (Integer) : Référence à l'identifiant d'un objet 'ZoneTable'.
            id_style (Integer) : Référence à l'identifiant d'un objet 'Style'.
            zone_table (Relationship) : Référence à l'objet 'ZoneTable' associé. La fonction 'backref' crée une liste d'objets 'Ligne' dans cet objet.
            style (Relationship) : Référence à l'objet 'Style' associé.
            ** cellules (List) : Liste d'objets 'Cellule' (créée par la fonction 'backref' lancée par la classe 'Cellule').
    """
    __tablename__ = 'Lignes'
    id = Column(Integer, primary_key=True)
    id_zone_table = Column(Integer, ForeignKey('ZonesTable.id', onupdate='cascade', ondelete='cascade'))
    id_style = Column(Integer, ForeignKey('Styles.id', onupdate='cascade', ondelete='set default'), default=5)
    zone_table = relationship(
        ZoneTable, 
        backref=backref(
            'lignes', 
            uselist=True, 
            cascade='delete,all'), 
        foreign_keys=[id_zone_table]
        )
    style = relationship(
        Style,
        uselist=False,
        foreign_keys=[id_style]
    )

    def serialiser_en_json(self):
        cellules_data = []
        data = dict(
            id = self.id,
            id_style = self.id_style
            #id_zone_table = self.id_zone_table PAS NECESSAIRE??
            )
        for cellule in self.cellules:
            cellules_data.append(cellule.serialiser_en_json())
        data['cellules'] = cellules_data
        return data

    def deserialiser_de_json(self, session, data):
        if (self.id_style != data['id_style']):
            self.style = session.query(Style).filter(Style.id == data['id_style']).one()
        for cellule in data['cellules']:
            if cellule['id'] == 0:
                print('Nouvelle cellule')
                nouvelle_cellule = Cellule(ligne=self)
                nouvelle_cellule.deserialiser_de_json(session, cellule)
                session.add(nouvelle_cellule)
            elif cellule['id'] > 0:
                session.query(Cellule).filter(Cellule.id == cellule['id']).one().deserialiser_de_json(session, cellule)
            elif cellule['id'] < 0:
                session.delete(session.query(Cellule).filter(Cellule.id == -cellule['id']).one())
            else:
                print('Impossible de déserialiser la cellule')
    
class Cellule(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Correspond à une cellule d'une 'Ligne'.
        
        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            contenu (String) : Texte contenu dans la cellule.
            id_ligne_table (Integer) : Référence à l'identifiant d'un objet 'Ligne'.
            id_style (Integer) : Référence à l'identifiant d'un objet 'Style'.
            ligne (Relationship) : Référence à l'objet 'Ligne' associé. La fonction 'backref' crée une liste d'objets 'Cellule' dans cet objet.
            style (Relationship) : Référence à l'objet 'Style' associé.
    """
    __tablename__ = 'Cellules'
    id = Column(Integer, primary_key=True)
    contenu = Column(String(150), default="")
    id_ligne = Column(Integer, ForeignKey('Lignes.id', onupdate='cascade', ondelete='cascade'))
    id_style = Column(Integer, ForeignKey('Styles.id', onupdate='cascade', ondelete='set default'), default=8)
    ligne = relationship(
        Ligne, 
        backref=backref(
            'cellules', 
            uselist=True, 
            cascade='delete,all'),
        foreign_keys=[id_ligne]
        )
    style = relationship(
        Style,
        uselist=False,
        foreign_keys=[id_style]
    )

    def serialiser_en_json(self):
        return dict(
            id = self.id,
            contenu = self.contenu,
            id_style = self.id_style
            )

    def deserialiser_de_json(self, session, data):
        if data.get('contenu') != None : self.contenu = data['contenu']
        if (self.id_style != data['id_style']):
            self.style = session.query(Style).filter(Style.id == data['id_style']).one()

class Administrateur(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Sert à l'authentification d'un utilisateur dans le système.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            adresse_courriel (String) : Courriel qui sert à la récupération du mot de passe.
            mot_de_passe (String) : Phrase de sécurité. Est nécessaire pour l'authentification d'un administrateur au système de gestion.
    """
    __tablename__ = 'Administrateurs'
    id = Column(Integer, primary_key=True)
    adresse_courriel = Column(String, default='da.junior.du@gmail.com') #CHANGER LA VALEUR PAR DEFAUT
    mot_de_passe = Column(String, default='admin') #PAS SÉCURE

    def serialiser_en_json(self):
        return dict(
            id = self.id,
            adresse_courriel = self.adresse_courriel
            mot_de_passe = self.mot_de_passe,
            )

    def deserialiser_de_json(self, session, data):
        if data.get('adresse_courriel') != None : self.adresse_courriel = data['adresse_courriel']
        if data.get('mot_de_passe') != None : self.mot_de_passe = data['mot_de_passe']
#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class Media(Base):
    __tablename__ = 'Medias'
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    chemin_fichier = Column(String)
    type = Column(String)

    def serialiser_en_json(self):
        return dict(
            id = self.id,
            nom = self.nom,
            chemin_fichier = self.chemin_fichier,
            type=self.type)

    def deserialiser_de_json(self, session, data):
        self.nom = data['nom']
        self.chemin_fichier = data['chemin_fichier']
        self.type = data['type']

class Bordure(Base):
    __tablename__ = 'Bordures'
    id = Column(Integer, primary_key=True)
    couleur = Column(String(250), default='#000000')
    taille = Column(String(250), default='0px')
    style = Column(String(250), default='solid')

    def serialiser_en_json(self):
        return dict(
            id = self.id,
            couleur = self.couleur,
            taille = self.taille,
            style = self.style
            )

    def deserialiser_de_json(self, session, data):
            self.couleur = data['couleur']
            self.taille = data['taille']
            self.style = data['style']

class Style(Base):
    __tablename__ = 'Styles'
    id = Column(Integer, primary_key=True)
    police = Column(String(250), default='1.5vw')
    couleur = Column(String(250), default='#000000')
    taille = Column(Integer, default='1.5vw')
    couleur_fond = Column(String(250), default='#FFFFFF')
    opacite_fond = Column(Integer, default='0')
    gras = Column(String(250), default='normal')
    italique = Column(String(250), default='normal')
    bordure_id = Column(
        Integer, 
        ForeignKey('Bordures.id'),
        nullable=False
        )
    bordure = relationship(
        Bordure, 
        uselist=False, 
        cascade='delete,all'
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
            bordure = self.bordure.serialiser_en_json()
            )

    def deserialiser_de_json(self, session, data):
        self.police = data['police']
        self.couleur = data['couleur']
        self.taille = data['taille']
        self.couleur_fond = data['couleur_fond']
        self.opacite_fond = data['opacite_fond']
        self.gras = data['gras']
        self.italique = data['italique']
        self.bordure.deserialiser_de_json(session, data['bordure'])

class Theme(Base):
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
        ForeignKey('Styles.id'),
        nullable=False
        )
    id_sous_titre = Column(
        Integer, 
        ForeignKey('Styles.id'),
        nullable=False
        )
    id_texte = Column(
        Integer, 
        ForeignKey('Styles.id'),
        nullable=False
        )
    id_tableau = Column(
        Integer, 
        ForeignKey('Styles.id'),
        nullable=False
        )
    id_tableau_ligne = Column(
        Integer, 
        ForeignKey('Styles.id'),
        nullable=False
        )
    id_tableau_titre = Column(
        Integer, 
        ForeignKey('Styles.id'),
        nullable=False
        )
    id_tableau_sous_titre = Column(
        Integer, 
        ForeignKey('Styles.id'),
        nullable=False
        )
    id_tableau_texte = Column(
        Integer, 
        ForeignKey('Styles.id'),
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
            self.nom = data['nom']
            self.titre.deserialiser_de_json(session, data['titre'])
            self.sous_titre.deserialiser_de_json(session, data['sous_titre'])
            self.texte.deserialiser_de_json(session, data['texte'])
            self.tableau.deserialiser_de_json(session, data['tableau'])
            self.tableau_ligne.deserialiser_de_json(session, data['tableau_ligne'])
            self.tableau_titre.deserialiser_de_json(session, data['tableau_titre'])
            self.tableau_sous_titre.deserialiser_de_json(session, data['tableau_sous_titre'])
            self.tableau_texte.deserialiser_de_json(session, data['tableau_texte'])

class Fenetre(Base):
    __tablename__ = 'Fenetres'
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    fond = Column(String)
    id_theme = Column(Integer, ForeignKey('Themes.id'))  
    theme = relationship(Theme, foreign_keys=[id_theme])

    def serialiser_en_json(self):
        zones_data = []
        data = dict(
            id = self.id,
            nom = self.nom,
            fond = self.fond,
            theme = self.theme.serialiser_en_json()
            )
        for zone in self.zones:
            zones_data.append(zone.serialiser_en_json())
        data['zones'] = zones_data
        return data

    def deserialiser_de_json(self, session, data):
        self.nom = data['nom']
        self.fond = data['fond']
        if(self.theme != data['theme']['id']):
            self.theme = session.query(Theme).filter(Theme.id == data['theme']['id']).one()

class Periode(Base):
    __tablename__ = 'Periodes'
    id = Column(Integer, primary_key=True)
    heure_debut = Column(DateTime)
    id_fenetre_1 = Column(Integer, ForeignKey('Fenetres.id'))
    id_fenetre_2 = Column(Integer, ForeignKey('Fenetres.id'))
    id_fenetre_3 = Column(Integer, ForeignKey('Fenetres.id'))
    id_fenetre_4 = Column(Integer, ForeignKey('Fenetres.id'))
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
        self.heure_debut = data['heure_debut']
        if(self.fenetre_1 != data['fenetre_1']['id']):
            self.fenetre_1 = session.query(Fenetre).filter(Fenetre.id == data['fenetre_1']['id']).one()
        if(self.fenetre_2 != data['fenetre_2']['id']):
            self.fenetre_2 = session.query(Fenetre).filter(Fenetre.id == data['fenetre_2']['id']).one()
        if(self.fenetre_3 != data['fenetre_3']['id']):
            self.fenetre_3 = session.query(Fenetre).filter(Fenetre.id == data['fenetre_3']['id']).one()
        if(self.fenetre_4 != data['fenetre_4']['id']):
            self.fenetre_4 = session.query(Fenetre).filter(Fenetre.id == data['fenetre_4']['id']).one()


class Zone(Base):
    __tablename__ = 'Zones'
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    position_x = Column(String)
    position_y = Column(String)
    largeur = Column(String)
    hauteur = Column(String)
    type = Column(String(50))
    id_fenetre = Column(Integer, ForeignKey('Fenetres.id'))
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
    __tablename__ = 'ZonesBase'
    id = Column(Integer, ForeignKey('Zones.id'), primary_key=True)
    contenu = Column(String)
    id_style = Column(Integer, ForeignKey('Styles.id'))
    style = relationship(
        Style,
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_style]
    )

    def serialiser_en_json(self):
        return dict(
            id = self.id,
            contenu = self.contenu,
            nom = self.nom,
            position_x = self.position_x,
            position_y = self.position_y,
            largeur = self.largeur,
            hauteur = self.hauteur,
            type = self.type,
            id_style = self.id_style,
            id_fenetre = self.id_fenetre
            )

    def deserialiser_de_json(self, session, data):
        self.contenu = data['contenu']
        self.nom = data['nom']
        self.position_x = data['position_x']
        self.position_y = data['position_y']
        self.largeur = data['largeur']
        self.hauteur = data['hauteur']
        self.type = data['type']
        self.style = session.query(Style).filter(Style.id == data['id_style']).one()
        # self.fenetre ** ON NE PEUT PAS CHANGER LA FENETRE D'UNE ZONE

    __mapper_args__ = {
        'polymorphic_identity':'ZoneBase',
    }

class ZoneImage(Zone):
    __tablename__ = 'ZonesImage'
    id = Column(Integer, ForeignKey('Zones.id'), primary_key=True)
    id_media = Column(Integer, ForeignKey('Medias.id'))
    image = relationship(Media)

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
            id_fenetre=self.id_fenetre,
            image = self.image.serialiser_en_json()
            )

    def deserialiser_de_json(self, session, data):
        self.image = session.query(Media).filter(Media.id == data['media']['id']).one()
        self.nom = data['nom']
        self.position_x = data['position_x']
        self.position_y = data['position_y']
        self.largeur = data['largeur']
        self.hauteur = data['hauteur']
        self.type = data['type']
        # self.fenetre ** ON NE PEUT PAS CHANGER LA FENETRE D'UNE ZONE


class ZoneVideo(Zone):
    __tablename__ = 'ZonesVideo'
    id = Column(Integer, ForeignKey('Zones.id'), primary_key=True)
    id_media = Column(Integer, ForeignKey('Medias.id'))
    video = relationship(Media)

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
            id_fenetre=self.id_fenetre,
            media = self.video.serialiser_en_json()
            )

    def deserialiser_de_json(self, session, data):
        self.video = session.query(Media).filter(Media.id == data['media']['id']).one()
        self.nom = data['nom']
        self.position_x = data['position_x']
        self.position_y = data['position_y']
        self.largeur = data['largeur']
        self.hauteur = data['hauteur']
        self.type = data['type']
        # self.fenetre ** ON NE PEUT PAS CHANGER LA FENETRE D'UNE ZONE

class ZoneTable(Zone):
    __tablename__ = 'ZonesTable'
    id = Column(Integer, ForeignKey('Zones.id'), primary_key=True)
    id_style = Column(Integer, ForeignKey('Styles.id'))
    style = relationship(
        Style,
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_style]
    )

    __mapper_args__ = {
        'polymorphic_identity':'ZoneTable',
    }

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
            id_style = self.id_style,
            id_fenetre=self.id_fenetre
            )
        for ligne in self.lignes:
            lignes_data.append(ligne.serialiser_en_json())
        data['lignes'] = lignes_data
        return data

    def deserialiser_de_json(self, session, data):
        self.nom = data['nom']
        self.position_x = data['position_x']
        self.position_y = data['position_y']
        self.largeur = data['largeur']
        self.hauteur = data['hauteur']
        self.type = data['type']
        self.style = session.query(Style).filter(Style.id == data['id_style']).one()
        for ligne in data['lignes']:
            if (ligne['id'] == ""):
                print('Nouvelle ligne')
                nouvelle_ligne = Ligne(zone_table=self, style=self.fenetre.theme.tableau_ligne)
                session.add(nouvelle_ligne)
                for cellule in ligne['cellules']:
                    print('Nouvelle cellule')
                    session.add(
                        Cellule(
                            contenu=cellule['contenu'],
                            ligne=nouvelle_ligne,
                            style=self.fenetre.theme.tableau_texte # DÉFINIR LE THEME A ASSOCIER À CHAQUE CELLULE
                            )
                        )
            else:
                session.query(Ligne).filter(Ligne.id == ligne['id']).one().deserialiser_de_json(ligne) # REQUETE POUR CHAQUE CELLULE??
        # self.fenetre ** ON NE PEUT PAS CHANGER LA FENETRE D'UNE ZONE

class Ligne(Base):
    __tablename__ = 'Lignes'
    id = Column(Integer, primary_key=True)
    id_zone_table = Column(Integer, ForeignKey('ZonesTable.id'))
    id_style = Column(Integer, ForeignKey('Styles.id'))
    zone_table = relationship(
        ZoneTable, 
        backref=backref(
            'lignes', 
            uselist=True, 
            cascade='delete,all')
        )
    style = relationship(
        Style,
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_style]
    )

    def serialiser_en_json(self):
        cellules_data = []
        data = dict(
            id = self.id,
            id_style = self.id_style,
            id_zone_table = self.id_zone_table
            )
        for cellule in self.cellules:
            cellules_data.append(cellule.serialiser_en_json())
        data['cellules'] = cellules_data
        return data

    def deserialiser_de_json(self, session, data):
        self.style = session.query(Style).filter(Style.id == data['id_style']).one()
        for cellule in data['cellules']:
            cellule = session.query(Style).filter(Style.id == data['id_style']).one()
        # self.zone_table ** ON NE PEUT PAS CHANGER LA ZONE D'UNE LIGNE
    
class Cellule(Base):
    __tablename__ = 'Cellules'
    id = Column(Integer, primary_key=True)
    contenu = Column(String(150))
    id_ligne_table = Column(Integer, ForeignKey('Lignes.id'))
    id_style = Column(Integer, ForeignKey('Styles.id'))
    ligne = relationship(
        Ligne, 
        backref=backref(
            'cellules', 
            uselist=True, 
            cascade='delete,all')
        )
    style = relationship(
        Style,
        uselist=False, 
        cascade='delete,all', 
        foreign_keys=[id_style]
    )

    def serialiser_en_json(self):
        return dict(
            id = self.id,
            contenu = self.contenu,
            id_style = self.id_style,
            id_ligne_table = self.id_ligne_table
            )

    def deserialiser_de_json(self, session, data):
        self.contenu = data['contenu']
        self.style = session.query(Style).filter(Style.id == data['id_style']).one()
        self.ligne = session.query(Ligne).filter(Ligne.id == data['id_ligne_table']).one()

class Administrateur(Base):
    __tablename__ = 'Administrateurs'
    id = Column(Integer, primary_key=True)
    mot_de_passe = Column(String)
    adresse_courriel = Column(String)

    def serialiser_en_json(self):
        return dict(
            id = self.id,
            mot_de_passe = self.mot_de_passe,
            adresse_courriel = self.adresse_courriel
            )

    def deserialiser_de_json(self, session, data):
        self.mot_de_passe = data['mot_de_passe']
        self.adresse_courriel = data['adresse_courriel']

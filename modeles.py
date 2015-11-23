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
            chemin_fichier = self.chemin_fichier)

    def deserialiser_de_json(self, session, data):
        if data['id'] == -1:
            session.delete(self)
        else:
            self.nom = data['nom']
            self.chemin_fichier = data['chemin_fichier']
        
    __mapper_args__ = {
        'polymorphic_identity':'Media',
        'polymorphic_on':type
    }

class Image(Media):
    __tablename__ = 'Images'
    id = Column(Integer, ForeignKey('Medias.id'), primary_key=True)
        
    __mapper_args__ = {
        'polymorphic_identity':'Image'
    }

class Video(Media):
    __tablename__ = 'Videos'
    id = Column(Integer, ForeignKey('Medias.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'Video'
    }

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
        if data['id'] == -1:
            session.delete(self)
        else:
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
        if data['id'] == -1:
            session.delete(self)
        else:
            self.police = data['police']
            self.couleur = data['couleur']
            self.taille = data['taille']
            self.couleur_fond = data['couleur_fond']
            self.opacite_fond = data['opacite_fond']
            self.gras = data['gras']
            self.italique = data['italique']
        if (data['bordure']['id'] == ""):
            nouvelle_bordure = Bordure()
            nouvelle_bordure.deserialiser_de_json(session, data['bordure'])
            session.add(nouvelle_bordure)
            self.bordure = nouvelle_bordure
        else:
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
            if data['id'] == -1:
                session.delete(self)
            else:
                self.nom = data['nom']

                # ----- VOIR SI IL N'Y A PAS UNE FACON PLUS EFFICACE DE CRÉER DE NOUVEAUX THEMES ------

                if (data['titre']['id'] == ""):
                    print('Nouveau style')
                    nouveau_style = Style()
                    nouveau_style.deserialiser_de_json(session, data['titre'])
                    session.add(nouveau_style)
                    self.titre = nouveau_style
                else:
                    self.titre.deserialiser_de_json(session, data['titre'])
                if (data['sous_titre']['id'] == ""):
                    print('Nouveau style')
                    nouveau_style = Style()
                    nouveau_style.deserialiser_de_json(session, data['sous_titre'])
                    session.add(nouveau_style)
                    self.sous_titre = nouveau_style
                else:    
                    self.sous_titre.deserialiser_de_json(session, data['sous_titre'])
                if (data['texte']['id'] == ""):
                    print('Nouveau style')
                    nouveau_style = Style()
                    nouveau_style.deserialiser_de_json(session, data['texte'])
                    session.add(nouveau_style)
                    self.texte = nouveau_style
                else:
                    self.texte.deserialiser_de_json(session, data['texte'])
                if (data['tableau']['id'] == ""):
                    print('Nouveau style')
                    nouveau_style = Style()
                    nouveau_style.deserialiser_de_json(session, data['tableau'])
                    session.add(nouveau_style)
                    self.tableau = nouveau_style
                else:
                    self.tableau.deserialiser_de_json(session, data['tableau'])
                if (data['tableau_ligne']['id'] == ""):
                    print('Nouveau style')
                    nouveau_style = Style()
                    nouveau_style.deserialiser_de_json(session, data['tableau_ligne'])
                    session.add(nouveau_style)
                    self.tableau_ligne = nouveau_style
                else:
                    self.tableau_ligne.deserialiser_de_json(session, data['tableau_ligne'])
                if (data['tableau_titre']['id'] == ""):
                    print('Nouveau style')
                    nouveau_style = Style()
                    nouveau_style.deserialiser_de_json(session, data['tableau_titre'])
                    session.add(nouveau_style)
                    self.tableau_titre = nouveau_style
                else:
                    self.tableau_titre.deserialiser_de_json(session, data['tableau_titre'])
                if (data['tableau_sous_titre']['id'] == ""):
                    print('Nouveau style')
                    nouveau_style = Style()
                    nouveau_style.deserialiser_de_json(session, data['tableau_sous_titre'])
                    session.add(nouveau_style)
                    self.tableau_sous_titre = nouveau_style
                else:
                    self.tableau_sous_titre.deserialiser_de_json(session, data['tableau_sous_titre'])
                if (data['tableau_texte']['id'] == ""):
                    print('Nouveau style')
                    nouveau_style = Style()
                    nouveau_style.deserialiser_de_json(session, data['tableau_texte'])
                    session.add(nouveau_style)
                    self.tableau_texte = nouveau_style
                else:
                    self.tableau_texte.deserialiser_de_json(session, data['tableau_texte'])

                # ----- VOIR SI IL N'Y A PAS UNE FACON PLUS EFFICACE DE CRÉER DE NOUVEAUX THEMES ------

class Fenetre(Base):
    __tablename__ = 'Fenetres'
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    id_image_fond = Column(Integer, ForeignKey('Images.id'))  
    couleur_fond = Column(String)
    id_theme = Column(Integer, ForeignKey('Themes.id'))  
    theme = relationship(Theme, foreign_keys=[id_theme])
    image_fond = relationship(Image, foreign_keys=[id_image_fond])

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
        if data['id'] == -1:
            session.delete(self)
        else:
            self.nom = data['nom']
            self.couleur_fond = data['couleur_fond']
            if (self.id_theme != data['theme']['id']):
                if (data['theme']['id'] == ""):
                    print('Nouveau theme')
                    nouveau_theme = Theme()
                    nouveau_theme.deserialiser_de_json(session, data['theme'])
                    session.add(nouveau_theme)
                    self.theme = nouveau_theme
                else:
                    self.theme = session.query(Theme).filter(Theme.id == data['theme']['id']).one()
            if (self.id_image_fond != data['image_fond']['id']):
                if (data['image_fond']['id'] == ""):
                    nouvelle_image_fond = Image()
                    nouvelle_image_fond.deserialiser_de_json(session, data['image_fond'])
                    session.add(nouvelle_image_fond)
                    self.image_fond = nouvelle_image_fond
                else:
                    self.image_fond = session.query(Image).filter(Image.id == data['image_fond']['id']).one()
            for zone in data['zones']:
                if zone['id'] == "":
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
                else:
                    session.query(Zone).filter(Zone.id == zone['id']).one().deserialiser_de_json(session, zone)

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
        if data['id'] == -1:
            session.delete(self)
        else:
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
            id_style = self.id_style
            )

    def deserialiser_de_json(self, session, data):
        if data['id'] == -1:
            session.delete(self)
        else:
            self.contenu = data['contenu']
            self.nom = data['nom']
            self.position_x = data['position_x']
            self.position_y = data['position_y']
            self.largeur = data['largeur']
            self.hauteur = data['hauteur']
            self.style = session.query(Style).filter(Style.id == data['id_style']).one()

    __mapper_args__ = {
        'polymorphic_identity':'ZoneBase',
    }

class ZoneImage(Zone):
    __tablename__ = 'ZonesImage'
    id = Column(Integer, ForeignKey('Zones.id'), primary_key=True)
    id_image = Column(Integer, ForeignKey('Images.id'))
    image = relationship(Image)

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
        if data['id'] == -1:
            session.delete(self)
        else:
            if (self.id_image != data['image']['id']):
                if data['image']['id'] == "":
                    nouvelle_image = Image()
                    nouvelle_image.deserialiser_de_json(session, data['image'])
                    session.add(nouvelle_image)
                    self.image = nouvelle_image
                else:
                    self.image = session.query(Image).filter(Image.id == data['image']['id']).one()
            self.nom = data['nom']
            self.position_x = data['position_x']
            self.position_y = data['position_y']
            self.largeur = data['largeur']
            self.hauteur = data['hauteur']

class ZoneVideo(Zone):
    __tablename__ = 'ZonesVideo'
    id = Column(Integer, ForeignKey('Zones.id'), primary_key=True)
    id_video = Column(Integer, ForeignKey('Videos.id'))
    video = relationship(Video)

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
        if data['id'] == -1:
            session.delete(self)
        else:
            if (self.id_video != data['video']['id']):
                if data['video']['id'] == "":
                    nouvelle_video = Video()
                    nouvelle_video.deserialiser_de_json(session, data['video'])
                    session.add(nouvelle_video)
                    self.video = nouvelle_video
                else:
                    self.video = session.query(Video).filter(Video.id == data['video']['id']).one()
            self.nom = data['nom']
            self.position_x = data['position_x']
            self.position_y = data['position_y']
            self.largeur = data['largeur']
            self.hauteur = data['hauteur']

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
            id_style = self.id_style
            )
        for ligne in self.lignes:
            lignes_data.append(ligne.serialiser_en_json())
        data['lignes'] = lignes_data
        return data

    def deserialiser_de_json(self, session, data):
        if data['id'] == -1:
            session.delete(self)
        else:
            self.nom = data['nom']
            self.position_x = data['position_x']
            self.position_y = data['position_y']
            self.largeur = data['largeur']
            self.hauteur = data['hauteur']
            if self.id_style != data['id_style']:
                self.style = session.query(Style).filter(Style.id == data['id_style']).one()
            for ligne in data['lignes']:
                if (ligne['id'] == ""):
                    print('Nouvelle ligne')
                    nouvelle_ligne = Ligne(zone_table=self)
                    nouvelle_ligne.deserialiser_de_json(session, ligne)
                    session.add(nouvelle_ligne)
                else:
                    session.query(Ligne).filter(Ligne.id == ligne['id']).one().deserialiser_de_json(session, ligne) # REQUETE POUR CHAQUE CELLULE??

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
            id_style = self.id_style
            #id_zone_table = self.id_zone_table PAS NECESSAIRE??
            )
        for cellule in self.cellules:
            cellules_data.append(cellule.serialiser_en_json())
        data['cellules'] = cellules_data
        return data

    def deserialiser_de_json(self, session, data):
        if data['id'] == -1:
            session.delete(self)
        else:
            self.style = session.query(Style).filter(Style.id == data['id_style']).one()
            for cellule in data['cellules']:
                if cellule['id'] == "":
                    print('Nouvelle cellule')
                    nouvelle_cellule = Cellule(ligne=self)
                    nouvelle_cellule.deserialiser_de_json(session, cellule)
                    session.add(nouvelle_cellule)
                else:
                    session.query(Cellule).filter(Cellule.id == cellule['id']).one().deserialiser_de_json(session, cellule)
    
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
            id_style = self.id_style
            # id_ligne_table = self.id_ligne_table PAS NECESSAIRE??
            )

    def deserialiser_de_json(self, session, data):
        if data['id'] == -1:
            session.delete(self)
        else:
            self.contenu = data['contenu']
            self.style = session.query(Style).filter(Style.id == data['id_style']).one()

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
        if data['id'] == -1:
            session.delete(self)
        else:
            self.mot_de_passe = data['mot_de_passe'] # CRYPTER LE MOT DE PASSE DANS LA BD
            self.adresse_courriel = data['adresse_courriel']

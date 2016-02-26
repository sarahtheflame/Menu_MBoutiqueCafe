#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Création d'objets dans la base de données servant d'exemples
    Fait par : Daniel-Junior Dubé et Sarah Laflamme
    Date : 10-12-2015
"""
__author__ = 'Daniel-Junior Dubé & Sarah Laflamme'

import datetime
from modeles.media import Media
from modeles.image import Image
from modeles.video import Video
from modeles.bordure import Bordure
from modeles.style import Style
from modeles.theme import Theme
from modeles.fenetre import Fenetre
from modeles.periode import Periode
from modeles.zone import Zone
from modeles.zone_base import ZoneBase
from modeles.zone_image import ZoneImage
from modeles.zone_video import ZoneVideo
from modeles.zone_table import ZoneTable
from modeles.ligne import Ligne
from modeles.cellule import Cellule
from modeles.administrateur import Administrateur
from modeles.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker

engine = create_engine('sqlite:///src//data//database.db', encoding='utf8', convert_unicode=True)
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)

s = session()

theme_1 = Theme(
    nom='Thème principal #1',
    titre=Style(
        police="KaushanScript-Regular",
        couleur="#ff7400",
        taille="28",
        couleur_fond="#000000",
        opacite_fond="0.8",
        gras="bold",
        italique="italic",
        soulignement="underline",
        type="titre",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0",
            style="solid"
        )
    ),
    sous_titre=Style(
        police="Oswald-Regular",
        couleur="#ff8f32",
        taille="20",
        couleur_fond="",
        opacite_fond="1",
        type="sous_titre",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0",
            style="solid"
        )
    ),
    texte=Style(
        police="Oswald-Regular",
        couleur="#FFFFFF",
        taille="14",
        couleur_fond="",
        opacite_fond="1",
        type="texte",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0",
            style="solid"
        )
    ),
    tableau=Style(
        police="Oswald-Regular",
        couleur="#FFFFFF",
        taille="14",
        couleur_fond="#000000",
        opacite_fond="0.8",
        type="tableau",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0",
            style="solid"
        )
    ),
    tableau_ligne=Style(
        police="Oswald-Regular",
        couleur="#FFFFFF",
        taille="14",
        couleur_fond="",
        opacite_fond="1",
        type="tableau_ligne",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0",
            style="solid"
        )
    ),
    tableau_titre=Style(
        police="Oswald-Regular",
        couleur="#ff8f32",
        taille="26",
        couleur_fond="",
        opacite_fond="1",
        gras="bold",
        soulignement="underline",
        type="tableau_titre",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0",
            style="solid"
        )
    ),
    tableau_sous_titre=Style(
        police="Oswald-Regular",
        couleur="#ff8f32",
        taille="18",
        couleur_fond="",
        opacite_fond="1",
        italique="italic",
        type="tableau_sous_titre",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0",
            style="solid"
        )
    ),
    tableau_texte=Style(
        police="Oswald-Regular",
        couleur="#FFFFFF",
        taille="14",
        couleur_fond="",
        opacite_fond="1",
        type="tableau_texte",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0",
            style="solid"
        )
    )
)
theme_2 = Theme(
    nom='Thème secondaire',
    titre=Style(
        police="KaushanScript-Regular",
        couleur="#ff7400",
        taille="32",
        couleur_fond="#000000",
        opacite_fond="0.8",
        gras="bold",
        italique="italic",
        type="titre",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0",
            style="solid"
        )
    ),
    sous_titre=Style(
        police="Oswald-Regular",
        couleur="#ff8f32",
        taille="26",
        couleur_fond="",
        opacite_fond="1",
        soulignement="underline",
        type="sous_titre",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0",
            style="solid"
        )
    ),
    texte=Style(
        police="Oswald-Regular",
        couleur="#FFFFFF",
        taille="16",
        couleur_fond="",
        opacite_fond="1",
        type="texte",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0",
            style="solid"
        )
    ),
    tableau=Style(
        police="Oswald-Regular",
        couleur="#FFFFFF",
        taille="14",
        couleur_fond="#000000",
        opacite_fond="0.8",
        type="tableau",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0",
            style="solid"
        )
    ),
    tableau_ligne=Style(
        police="Oswald-Regular",
        couleur="#FFFFFF",
        taille="14",
        couleur_fond="",
        opacite_fond="1",
        type="tableau_ligne",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0",
            style="solid"
        )
    ),
    tableau_titre=Style(
        police="Oswald-Regular",
        couleur="#ff8f32",
        taille="28",
        couleur_fond="",
        opacite_fond="1",
        type="tableau_titre",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0",
            style="solid"
        )
    ),
    tableau_sous_titre=Style(
        police="Oswald-Regular",
        couleur="#ff8f32",
        taille="22",
        couleur_fond="",
        opacite_fond="1",
        italique="italic",
        type="tableau_sous_titre",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0",
            style="solid"
        )
    ),
    tableau_texte=Style(
        police="Oswald-Regular",
        couleur="#FFFFFF",
        taille="18",
        couleur_fond="",
        opacite_fond="1",
        type="tableau_texte",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0",
            style="solid"
        )
    )
)

image_vide = Image(
    nom='vide', 
    chemin_fichier='vide.png'
)


image_sandwich_europeen = Image(
    nom='sandwich', 
    chemin_fichier='sandwich.jpg'
)

image_sandwich_europeen2 = Image(
    nom='cafe', 
    chemin_fichier='cafe.jpg'
)

video_cafe = Video(
    nom='Annonce Café', 
    chemin_fichier='coffee.mp4'
)

fenetre_repas = Fenetre(
    nom='Fenêtre Repas', 
    image_fond=image_sandwich_europeen, 
    couleur_fond = "#FFFFFF",
    theme=theme_2
)

fenetre_dessert = Fenetre(
    nom='Fenêtre Dessert', 
    image_fond=image_sandwich_europeen, 
    couleur_fond = "#FFFFFF",
    theme=theme_1
)

zone_entete = ZoneBase(
    nom='zone_grillwiches', 
    position_x=2,
    position_y=18,
    largeur=32,
    hauteur=78,
    fenetre=fenetre_repas,
    type_style="titre",
    contenu="Nos repas"
)

zone_grillwiches = ZoneTable(
    nom='zone_grillwiches', 
    nombre_colonnes=2,
    position_x=2,
    position_y=18,
    largeur=32,
    hauteur=78,
    fenetre=fenetre_repas
)

administrateur_1 = Administrateur(
    adresse_courriel='da.junior.du@gmail.com', 
    mot_de_passe="test"
)

administrateur_2 = Administrateur(
    adresse_courriel='test@gmail.com', 
    mot_de_passe="123"
)

administrateur_3 = Administrateur(
    adresse_courriel='allo@gmail.com', 
    mot_de_passe="allo"
)

ligne_1_grillwiches = Ligne(
        zone_table=zone_grillwiches
        )
cellule_1_ligne_1_grillwiches = Cellule(
        contenu="Nos Grill'wiches matin",
        ligne=ligne_1_grillwiches,
        type_style="tableau_titre"
        )
cellule_2_ligne_1_grillwiches = Cellule(
        contenu="",
        ligne=ligne_1_grillwiches,
        type_style="tableau_titre"
        )
ligne_2_grillwiches = Ligne(
        zone_table=zone_grillwiches
        )
cellule_1_ligne_2_grillwiches = Cellule(
        contenu="Fromage",
        ligne=ligne_2_grillwiches
        )
cellule_2_ligne_2_grillwiches = Cellule(
        contenu="5.00$",
        ligne=ligne_2_grillwiches
        )
ligne_3_grillwiches = Ligne(
        zone_table=zone_grillwiches
        )
cellule_1_ligne_3_grillwiches = Cellule(
        contenu="Fromage et fruit",
        ligne=ligne_3_grillwiches
        )
cellule_2_ligne_3_grillwiches = Cellule(
        contenu="5.00$",
        ligne=ligne_3_grillwiches
        )
ligne_4_grillwiches = Ligne(
        zone_table=zone_grillwiches
        )
cellule_1_ligne_4_grillwiches = Cellule(
        contenu="Oeuf bacon fromage",
        ligne=ligne_4_grillwiches
        )
cellule_2_ligne_4_grillwiches = Cellule(
        contenu="5.00$",
        ligne=ligne_4_grillwiches
        )
ligne_5_grillwiches = Ligne(
        zone_table=zone_grillwiches
        )
cellule_1_ligne_5_grillwiches = Cellule(
        contenu="Oeuf fromage",
        ligne=ligne_5_grillwiches
        )
cellule_2_ligne_5_grillwiches = Cellule(
        contenu="5.00$",
        ligne=ligne_5_grillwiches
        )
ligne_6_grillwiches = Ligne(
        zone_table=zone_grillwiches
        )
cellule_1_ligne_6_grillwiches = Cellule(
        contenu="Nos Grill'wiches diner",
        ligne=ligne_6_grillwiches,
        type_style="tableau_titre"
        )
cellule_2_ligne_6_grillwiches = Cellule(
        contenu="",
        ligne=ligne_6_grillwiches,
        type_style="tableau_titre"
        )
ligne_7_grillwiches = Ligne(
        zone_table=zone_grillwiches
        )
cellule_1_ligne_7_grillwiches = Cellule(
        contenu="Poulet club",
        ligne=ligne_7_grillwiches
)
cellule_2_ligne_7_grillwiches = Cellule(
        contenu="5.00$",
        ligne=ligne_7_grillwiches
)
ligne_8_grillwiches = Ligne(
        zone_table=zone_grillwiches
)
cellule_1_ligne_8_grillwiches = Cellule(
        contenu="Le pizza",
        ligne=ligne_8_grillwiches
)
cellule_2_ligne_8_grillwiches = Cellule(
        contenu="5.00$",
        ligne=ligne_8_grillwiches
)

zone_salade = ZoneTable(
    nom='zone salade', 
    nombre_colonnes=3,
    position_x=36,
    position_y=18,
    largeur=37,
    hauteur="",
    fenetre=fenetre_repas
)
ligne_1_salade = Ligne(
        zone_table=zone_salade
)
cellule_1_ligne_1_salade = Cellule(
        contenu="Salade repas",
        ligne=ligne_1_salade
)
cellule_2_ligne_1_salade = Cellule(
        contenu="",
        ligne=ligne_1_salade
)
ligne_2_salade = Ligne(
        zone_table=zone_salade
)
cellule_1_ligne_2_salade = Cellule(
        contenu="Choisissez 1,2,3 choix!",
        ligne=ligne_2_salade
)
cellule_2_ligne_2_salade = Cellule(
        contenu="5.00$",
        ligne=ligne_2_salade
)
ligne_3_salade = Ligne(
        zone_table=zone_salade
)
cellule_1_ligne_3_salade = Cellule(
        contenu="Choisissez votre option protéine!",
        ligne=ligne_3_salade
)
cellule_2_ligne_3_salade = Cellule(
        contenu="",
        ligne=ligne_3_salade
)
ligne_4_salade = Ligne(
        zone_table=zone_salade
)
cellule_1_ligne_4_salade = Cellule(
        contenu="Oeufs, poulet, jambon, saumon, saucisse, végé",
        ligne=ligne_4_salade
)
cellule_2_ligne_4_salade = Cellule(
        contenu="1.95$",
        ligne=ligne_4_salade
)

zone_test = ZoneTable(
    nom='zone test', 
    position_x=2,
    position_y=18,
    largeur=32,
    hauteur=78,
    fenetre=fenetre_repas
)
ligne_1_test = Ligne(
        zone_table=zone_test
)
cellule_1_ligne_1_test = Cellule(
        contenu="ceci est un test de ZoneTable",
        ligne=ligne_1_test
)
zone_test_image = ZoneImage(
    nom='zone test', 
    position_x=2,
    position_y=18,
    largeur=32,
    hauteur=78,
    fenetre=fenetre_repas,
    image=image_sandwich_europeen
)

periode1 = Periode(
    heure_debut = datetime.time(10, 21))

periode2 = Periode(
    heure_debut = datetime.time(13, 4))

periode3 = Periode(
    heure_debut = datetime.time(15, 1))

s.add_all([
    administrateur_1,
    administrateur_2,
    administrateur_3,
    video_cafe,
    image_vide,
    image_sandwich_europeen,
    image_sandwich_europeen2,
    theme_1,
    theme_2,
    fenetre_repas,
    zone_entete,
    zone_grillwiches,
    ligne_1_grillwiches,
    cellule_1_ligne_1_grillwiches,
    cellule_2_ligne_1_grillwiches,
    ligne_2_grillwiches,
    cellule_1_ligne_2_grillwiches,
    cellule_2_ligne_2_grillwiches,
    ligne_3_grillwiches,
    cellule_1_ligne_3_grillwiches,
    cellule_2_ligne_3_grillwiches,
    ligne_4_grillwiches,
    cellule_1_ligne_4_grillwiches,
    cellule_2_ligne_4_grillwiches,
    ligne_5_grillwiches,
    cellule_1_ligne_5_grillwiches,
    cellule_2_ligne_5_grillwiches,
    ligne_6_grillwiches,
    cellule_1_ligne_6_grillwiches,
    cellule_2_ligne_6_grillwiches,
    ligne_7_grillwiches,
    cellule_1_ligne_7_grillwiches,
    cellule_2_ligne_7_grillwiches,
    ligne_8_grillwiches,
    cellule_1_ligne_8_grillwiches,
    cellule_2_ligne_8_grillwiches,
    zone_salade,
    ligne_1_salade,
    cellule_1_ligne_1_salade,
    cellule_2_ligne_1_salade,
    ligne_2_salade,
    cellule_1_ligne_2_salade,
    cellule_2_ligne_2_salade,
    ligne_3_salade,
    cellule_1_ligne_3_salade,
    cellule_2_ligne_3_salade,
    ligne_4_salade,
    cellule_1_ligne_4_salade,
    cellule_2_ligne_4_salade,
    zone_test,
    ligne_1_test,
    cellule_1_ligne_1_test,
    zone_test_image,
    periode1,
    periode2,
    periode3]
)

s.commit()
#!/usr/bin/python
# -*- coding: utf-8 -*-

from modeles import *
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root@localhost/boutique')
#engine = create_engine('sqlite:///src//data//database.db', encoding='utf8', convert_unicode=True)
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)

s = session()

theme_1 = Theme(
    nom='theme principal',
    titre=Style(
        police="'KaushanScript', cursive",
        couleur="#ff7400",
        taille="4vw",
        couleur_fond="#000000",
        opacite_fond="0.8",
        gras="",
        italique="",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0px",
            style="solid"
        )
    ),
    sous_titre=Style(
        police="'Oswald', sans-serif",
        couleur="#ff8f32",
        taille="3vw",
        couleur_fond="",
        opacite_fond="1",
        gras="",
        italique="",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0px",
            style="solid"
        )
    ),
    texte=Style(
        police="'Oswald', sans-serif",
        couleur="#FFFFFF",
        taille="1.5vw",
        couleur_fond="",
        opacite_fond="1",
        gras="",
        italique="",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0px",
            style="solid"
        )
    ),
    tableau=Style(
        police="'Oswald', sans-serif",
        couleur="#FFFFFF",
        taille="1.5vw",
        couleur_fond="#000000",
        opacite_fond="0.8",
        gras="",
        italique="",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0px",
            style="solid"
        )
    ),
    tableau_ligne=Style(
        police="'Oswald', sans-serif",
        couleur="#FFFFFF",
        taille="1.5vw",
        couleur_fond="",
        opacite_fond="1",
        gras="",
        italique="",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="1px",
            style="solid"
        )
    ),
    tableau_titre=Style(
        police="'Oswald', sans-serif",
        couleur="#ff8f32",
        taille="2vw",
        couleur_fond="",
        opacite_fond="1",
        gras="",
        italique="",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0px",
            style="solid"
        )
    ),
    tableau_sous_titre=Style(
        police="'Oswald', sans-serif",
        couleur="#ff8f32",
        taille="1.5vw",
        couleur_fond="",
        opacite_fond="1",
        gras="",
        italique="italic",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0px",
            style="solid"
        )
    ),
    tableau_texte=Style(
        police="'Oswald', sans-serif",
        couleur="#FFFFFF",
        taille="1.5vw",
        couleur_fond="",
        opacite_fond="1",
        gras="",
        italique="",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0px",
            style="solid"
        )
    )
)
theme_2 = Theme(
    nom='theme secondaire',
    titre=Style(
        police="'KaushanScript', cursive",
        couleur="#ff7400",
        taille="4vw",
        couleur_fond="#000000",
        opacite_fond="0.8",
        gras="",
        italique="",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0px",
            style="solid"
        )
    ),
    sous_titre=Style(
        police="'Oswald', sans-serif",
        couleur="#ff8f32",
        taille="3vw",
        couleur_fond="",
        opacite_fond="1",
        gras="",
        italique="",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0px",
            style="solid"
        )
    ),
    texte=Style(
        police="'Oswald', sans-serif",
        couleur="#FFFFFF",
        taille="1.5vw",
        couleur_fond="",
        opacite_fond="1",
        gras="",
        italique="",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0px",
            style="solid"
        )
    ),
    tableau=Style(
        police="'Oswald', sans-serif",
        couleur="#FFFFFF",
        taille="1.5vw",
        couleur_fond="#000000",
        opacite_fond="0.8",
        gras="",
        italique="",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0px",
            style="solid"
        )
    ),
    tableau_ligne=Style(
        police="'Oswald', sans-serif",
        couleur="#FFFFFF",
        taille="1.5vw",
        couleur_fond="",
        opacite_fond="1",
        gras="",
        italique="",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="1px",
            style="solid"
        )
    ),
    tableau_titre=Style(
        police="'Oswald', sans-serif",
        couleur="#ff8f32",
        taille="2vw",
        couleur_fond="",
        opacite_fond="1",
        gras="",
        italique="",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0px",
            style="solid"
        )
    ),
    tableau_sous_titre=Style(
        police="'Oswald', sans-serif",
        couleur="#ff8f32",
        taille="1.5vw",
        couleur_fond="",
        opacite_fond="1",
        gras="",
        italique="italic",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0px",
            style="solid"
        )
    ),
    tableau_texte=Style(
        police="'Oswald', sans-serif",
        couleur="#FFFFFF",
        taille="1.5vw",
        couleur_fond="",
        opacite_fond="1",
        gras="",
        italique="",
        bordure=Bordure(
            couleur="#FFFFFF",
            taille="0px",
            style="solid"
        )
    )
)

image_sandwich_europeen = Media(
    nom='sandwich', 
    chemin_fichier='sandwich.jpg'
)
fenetre_repas = Fenetre(
    nom='fenetre_repas', 
    fond=image_sandwich_europeen.chemin_fichier, 
    theme=theme_1
)


zone_entete = ZoneBase(
    nom='zone_grillwiches', 
    position_x="2%",
    position_y="18%",
    largeur="32%",
    hauteur="78%",
    fenetre=fenetre_repas,
    style=theme_1.titre,
    contenu="Nos repas"
)

zone_grillwiches = ZoneTable(
    nom='zone_grillwiches', 
    position_x="2%",
    position_y="18%",
    largeur="32%",
    hauteur="78%",
    fenetre=fenetre_repas,
    style=theme_1.tableau
)
ligne_1_grillwiches = Ligne(
        zone_table=zone_grillwiches,
        style=theme_1.tableau_ligne
)
cellule_1_ligne_1_grillwiches = Cellule(
        contenu="Nos Grill'wiches matin",
        ligne=ligne_1_grillwiches,
        style=theme_1.tableau_titre
)
cellule_2_ligne_1_grillwiches = Cellule(
        contenu="",
        ligne=ligne_1_grillwiches,
        style=theme_1.tableau_titre
)
ligne_2_grillwiches = Ligne(
        zone_table=zone_grillwiches,
        style=theme_1.tableau_ligne
)
cellule_1_ligne_2_grillwiches = Cellule(
        contenu="Fromage",
        ligne=ligne_2_grillwiches,
        style=theme_1.tableau_texte
)
cellule_2_ligne_2_grillwiches = Cellule(
        contenu="5.00$",
        ligne=ligne_2_grillwiches,
        style=theme_1.tableau_texte
)
ligne_3_grillwiches = Ligne(
        zone_table=zone_grillwiches,
        style=theme_1.tableau_ligne
)
cellule_1_ligne_3_grillwiches = Cellule(
        contenu="Fromage et fruit",
        ligne=ligne_3_grillwiches,
        style=theme_1.tableau_texte
)
cellule_2_ligne_3_grillwiches = Cellule(
        contenu="5.00$",
        ligne=ligne_3_grillwiches,
        style=theme_1.tableau_texte
)
ligne_4_grillwiches = Ligne(
        zone_table=zone_grillwiches,
        style=theme_1.tableau_ligne
)
cellule_1_ligne_4_grillwiches = Cellule(
        contenu="Oeuf bacon fromage",
        ligne=ligne_4_grillwiches,
        style=theme_1.tableau_texte
)
cellule_2_ligne_4_grillwiches = Cellule(
        contenu="5.00$",
        ligne=ligne_4_grillwiches,
        style=theme_1.tableau_texte
)
ligne_5_grillwiches = Ligne(
        zone_table=zone_grillwiches,
        style=theme_1.tableau_ligne
)
cellule_1_ligne_5_grillwiches = Cellule(
        contenu="Oeuf fromage",
        ligne=ligne_5_grillwiches,
        style=theme_1.tableau_texte
)
cellule_2_ligne_5_grillwiches = Cellule(
        contenu="5.00$",
        ligne=ligne_5_grillwiches,
        style=theme_1.tableau_texte
)
ligne_6_grillwiches = Ligne(
        zone_table=zone_grillwiches,
        style=theme_1.tableau_ligne
)
cellule_1_ligne_6_grillwiches = Cellule(
        contenu="Nos Grill'wiches diner",
        ligne=ligne_6_grillwiches,
        style=theme_1.tableau_titre
)
cellule_2_ligne_6_grillwiches = Cellule(
        contenu="",
        ligne=ligne_6_grillwiches,
        style=theme_1.tableau_titre
)
ligne_7_grillwiches = Ligne(
        zone_table=zone_grillwiches,
        style=theme_1.tableau_ligne
)
cellule_1_ligne_7_grillwiches = Cellule(
        contenu="Poulet club",
        ligne=ligne_7_grillwiches,
        style=theme_1.tableau_texte
)
cellule_2_ligne_7_grillwiches = Cellule(
        contenu="5.00$",
        ligne=ligne_7_grillwiches,
        style=theme_1.tableau_texte
)
ligne_8_grillwiches = Ligne(
        zone_table=zone_grillwiches,
        style=theme_1.tableau_ligne
)
cellule_1_ligne_8_grillwiches = Cellule(
        contenu="Le pizza",
        ligne=ligne_8_grillwiches,
        style=theme_1.tableau_texte
)
cellule_2_ligne_8_grillwiches = Cellule(
        contenu="5.00$",
        ligne=ligne_8_grillwiches,
        style=theme_1.tableau_texte
)

zone_salade = ZoneTable(
    nom='zone salade', 
    position_x="36%",
    position_y="18%",
    largeur="37%",
    hauteur="",
    fenetre=fenetre_repas,
    style=theme_1.tableau
)
ligne_1_salade = Ligne(
        zone_table=zone_salade,
        style=theme_1.tableau_ligne
)
cellule_1_ligne_1_salade = Cellule(
        contenu="Salade repas",
        ligne=ligne_1_salade,
        style=theme_1.tableau_titre
)
cellule_2_ligne_1_salade = Cellule(
        contenu="",
        ligne=ligne_1_salade,
        style=theme_1.tableau_texte
)
ligne_2_salade = Ligne(
        zone_table=zone_salade,
        style=theme_1.tableau_ligne
)
cellule_1_ligne_2_salade = Cellule(
        contenu="Choisissez 1,2,3 choix!",
        ligne=ligne_2_salade,
        style=theme_1.tableau_texte
)
cellule_2_ligne_2_salade = Cellule(
        contenu="5.00$",
        ligne=ligne_2_salade,
        style=theme_1.tableau_texte
)
ligne_3_salade = Ligne(
        zone_table=zone_salade,
        style=theme_1.tableau_ligne
)
cellule_1_ligne_3_salade = Cellule(
        contenu="Choisissez votre option protéine!",
        ligne=ligne_3_salade,
        style=theme_1.tableau_titre
)
cellule_2_ligne_3_salade = Cellule(
        contenu="",
        ligne=ligne_3_salade,
        style=theme_1.tableau_texte
)
ligne_4_salade = Ligne(
        zone_table=zone_salade,
        style=theme_1.tableau_ligne
)
cellule_1_ligne_4_salade = Cellule(
        contenu="Oeufs, poulet, jambon, saumon, saucisse, végé",
        ligne=ligne_4_salade,
        style=theme_1.tableau_texte
)
cellule_2_ligne_4_salade = Cellule(
        contenu="1.95$",
        ligne=ligne_4_salade,
        style=theme_1.tableau_texte
)

print(cellule_1_ligne_4_salade.contenu)

s.add_all([
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
    cellule_2_ligne_4_salade]
)

s.commit()

# for attr in vars(fenetre_repas):
#     print(attr)
# print("------")
# for attr in vars(zone_1_repas):
#     print(attr)

#Système de gestion d'affichage de menu

Par : Daniel-Junior Dubé et Sarah Laflamme

###Voici les dépendances et comment les installer

- Python 3.4 avec pip
- Bottle (librairie python)
- SQLAlchemy (librairie python)
- SQLite3

##Installation

###Python 3.4 : 
1. Téléchargez et installer l'interpréteur suivant à l'aide du site officiel : 
https://www.python.org/downloads/release/python-340/

###Bottle :
1. Ouvrez une invite de commande en tant qu'administrateur.
2. Lancez la commande suivante : pip install Bottle.

###SQLAlchemy :
1. Ouvrez une invite de commande en tant qu'administrateur.
2. Lancez la commande suivante : pip install SQLAlchemy.

###SQLite3 :
1. Installez la version qui correspond à votre système d'exploitation grâce au lien suivant : https://www.sqlite.org/download.html

##Comment lancer le serveur :

1. Dans le répertoire racine du projet (où se trouve ce readme), lancez le fichier 'serveur.py' avec l'interpréteur python (commande : 'python serveur.py').
3. À l'aide d'un navigateur web, dirigez-vous vers l'URL 'localhost/', vous devriez voir la phrase 'Page d'exemple!' apparaître.

##Comment générer les données de la base de données :

1. Dans le répertoire racine du projet (où se trouve ce readme), ouvrez le dossier 'tests'.
2. Lancez le fichier 'creer_modeles_exemple.py' avec l'interpréteur python (commande : 'python creer_modeles_exemple.py').
3. Dans le répertoire racine du projet, ouvrez le répertoire 'src', puis ouvrez le répertoire 'data'.
4. À l'aide d'SQLite3, ouvrez la base de données 'database.db'.
5. À l'aide de commande SQLite, vous serez en mesure de voir que des données ont été ajoutées à la base de données.

##Quelques exemples : 
1. Dans le répertoire racine du projet (où se trouve ce readme), ouvrez le dossier 'tests'.
2. Lancez les fichiers 'exemple1.py', 'exemple2.py', 'exemple3.py' et 'exemple4.py' avec l'interpéteur Python (exemple : 'python exemple1.py')

#NOTE IMPORTANTE : 
Puisque nous sommes en train d'effectuer la division des modèles en modules séparés, nous avons créé un fichier nommé 'modeles_temporaire.py' afin de démontrer les fonctionnalités implémentées.
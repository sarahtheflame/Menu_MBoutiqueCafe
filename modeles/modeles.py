
class Media(Base):
    """
        Description: 
            Hérite de la classe 'Base' de SQLAlchemy. Est une classe abstraite qui contient les 
            informations de base communes à tous les types de médias.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Identifiant unique généré par SQLAlchemy.
            nom (String) : Nom de la zone.
            chemin_fichier (String) : Chemin de fichier (relatif au serveur) qui pointe vers la 
                ressource (ex: /src/images/exemple.png).
            type (String) : Type polymorphique du média (voir l'attribut '__mapper_args___').
            __mapper_args__ (Dictionary) : Contient les options qui configurent le polymorphisme de
                la classe.
    """
    __tablename__ = 'Medias'
    id = Column(Integer, primary_key=True)
    nom = Column(String, default="Media sans nom")
    chemin_fichier = Column(String)
    type = Column(String)

    def serialiser_en_json(self):
        """
            Retourne un 'Dict' en format 'JSON' contenant les attributs de la classe (Nécessaire 
            puisque SQLAlchemy modifie l'architecture du '__dict__' de l'objet)
        """
        return dict(
            id = self.id,
            nom = self.nom,
            chemin_fichier = self.chemin_fichier
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
        if data.get('nom') != None : self.nom = data['nom']
        if data.get('chemin_fichier') != None : self.chemin_fichier = data['chemin_fichier']
        
    __mapper_args__ = {
        'polymorphic_identity':'Media',
        'polymorphic_on':type
    }

class Image(Media):
    """
        Description: 
            Hérite de la classe 'Media'. Permet de différencier un média de type 'Image' des autres
            types.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Référence à l'identifiant unique d'un 'Media'.
            __mapper_args__ (Dictionary) : Contient les options qui configurent le polymorphisme de
                la classe.
    """
    __tablename__ = 'Images'
    id = Column(
        Integer, 
        ForeignKey('Medias.id', onupdate="cascade", ondelete="cascade"), 
        primary_key=True
        )
        
    __mapper_args__ = {
        'polymorphic_identity':'Image'
    }

class Video(Media):
    """
        Description: 
            Hérite de la classe 'Media'. Permet de différencier un média de type 'Video' des autres
            types.

        Attributs:
            __tablename__ (String) : Nom de la table qui sera créée dans la base de données.
            id (Integer) : Référence à l'identifiant unique d'un 'Media'.
            __mapper_args__ (Dictionary) : Contient les options qui configurent le polymorphisme de
                la classe.
    """
    __tablename__ = 'Videos'
    id = Column(
        Integer, 
        ForeignKey('Medias.id', onupdate="cascade", ondelete="cascade"), 
        primary_key=True
        )

    __mapper_args__ = {
        'polymorphic_identity':'Video'
    }
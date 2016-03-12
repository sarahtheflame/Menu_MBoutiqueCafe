/**
 * Fonction lancée lorsque la page est prête
 */
$(document).ready(function(){
	/**
	 * Liste contenant les choix de styles possibles pour une cellule. 
	 * nom : Nom affiché pour l'utilisateur
	 * attribut : Valeur attribuée à l'attribut style de la cellule
	 */
	viewModel.choix_style_cellule = ko.observableArray([
		{ nom: "Texte", attribut: "tableau_texte" },
	    { nom: "Sous-titre", attribut: "tableau_sous_titre" },
	    { nom: "Titre", attribut: "tableau_titre" }
	]);
});

/**
 * Création d'un nouveau thème avec un id à 0 et une liste de cellules vides dont le nombre 
 * correspond au nombre_colonnes de la zone 
 * Lancé lors d'un clic sur un élément qui porte la classe ajouter_ligne
 */
$("body").on("click", ".ajouter_ligne", function() {
	var context = ko.contextFor(this);

	var Cellule = function(){
		this.id = ko.observable(0);
		this.contenu = ko.observable();
		this.type_style = ko.observable();
	};

	var Ligne = function(){
		this.id = ko.observable(0);
		this.cellules = ko.observableArray([]);
	};

	var nouvelle_ligne = new Ligne();
	for (var i = 0; i < context.$root.zone.nombre_colonnes(); i++) {
		nouvelle_ligne.cellules.push(new Cellule());
	}

	context.$root.zone.lignes.push(nouvelle_ligne);
});

/**
 * Supprime la ligne en mettant son id négatif si la ligne est enregistrée ou en la retirant
 * directement de la liste si elle a été créée sans être appliquée
 * Lancé lors d'un clic sur un élément qui porte la classe retirer
 */
$("body").on("click", ".retirer", function() {
    var context = ko.contextFor(this),
        id = context.$data.id();
    if (id != 0) {
      context.$data.id(-id);
    } else {
      context.$root.zone.lignes.remove(context.$data);
    }
});
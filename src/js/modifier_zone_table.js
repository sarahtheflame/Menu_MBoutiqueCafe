$(document).ready(function(){
	viewModel.choixStyleCellule = ko.observableArray([
		{ nom: "Titre", attribut: "tableau_titre" },
	    { nom: "Sous-titre", attribut: "tableau_sous_titre" },
	    { nom: "Texte", attribut: "tableau_texte" }
	]);
});

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
		console.log(i);
	}

	context.$root.zone.lignes.push(nouvelle_ligne);
});

$("body").on("click", ".retirer", function() {
    var context = ko.contextFor(this),
        id = context.$data.id();
    console.log("contexte : " +context);
    console.log("id : " +id);
    if (id != 0) {
      context.$data.id(-id);
    } else {
      context.$root.zone.lignes.remove(context.$data);
    }
    console.log(context.$data.id());
});
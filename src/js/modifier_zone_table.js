$(document).ready(function(){
	viewModel.choixStyleCellule = ko.observableArray([
		{ nom: "Titre", attribut: "tableau_titre" },
	    { nom: "Sous-titre", attribut: "tableau_sous_titre" },
	    { nom: "Texte", attribut: "tableau_texte" }
	]);
});

$("body").on("click", ".ajouter_ligne", function() {
  // var context = ko.contextFor(this);
  // var Cellule = function(){
  // };

  // context.$root.zone.li.push(new Fenetre());
  $('[data-toggle="tooltip"]').tooltip({'placement': 'top'});
});
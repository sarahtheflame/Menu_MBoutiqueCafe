$(document).ready(function(){
	viewModel.choixStyleCellule = ko.observableArray([
		{ nom: "Titre", attribut: "tableau_titre" },
	    { nom: "Sous-titre", attribut: "tableau_sous_titre" },
	    { nom: "Texte", attribut: "tableau_texte" }
	]);
});
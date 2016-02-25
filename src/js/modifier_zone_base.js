/**
 * Liste contenant les choix de styles possibles pour une zone Base. 
 * nom : Nom affiché pour l'utilisateur
 * attribut : Valeur attribuée à l'attribut style de la zone
 */
viewModel.choix_style_zone = ko.observableArray([
	{ nom: "Titre", attribut: "titre" },
    { nom: "Sous-titre", attribut: "sous_titre" },
    { nom: "Texte", attribut: "texte" }
]);

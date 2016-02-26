/**
 * Fonction lancée lorsque la page est prête
 */
$(document).ready(function(){
	/**
	 * Liste contenant les choix de styles possibles pour une bordure. 
	 * nom : Nom affiché pour l'utilisateur
	 * attribut : Valeur attribuée à l'attribut style de la bordure
	 */
	viewModel.choixStyleBordure = ko.observableArray([
		{ nom: "Solide", attribut: "solid" },
	    { nom: "Pointillée", attribut: "dotted" },
	    { nom: "Aucune", attribut: "none" }
	]);

	/**
	 * Formatte la couleur sélectionnée par le sélecteur de couleur au format rgba et l'attribue à 
	 * l'attribut couleur de l'élément
	 * Lancé lors d'un changement de couleur du sélecteur de couleur
	 */
	$(function(){
	    $('.choix_couleur_texte').colorpicker().on('changeColor.colorpicker', function(event){
	  		var context = ko.contextFor(this);
	  		var nouvelle_couleur = "rgba("+event.color.toRGB().r+","+event.color.toRGB().g+","+event.color.toRGB().b+","+event.color.toRGB().a+")";
	  		context.$data.couleur(nouvelle_couleur);
		});
	});

	/**
	 * Formatte la couleur sélectionnée par le sélecteur de couleur au format rgba et l'attribue à 
	 * l'attribut couleur_bordure de l'élément
	 * Lancé lors d'un changement de couleur du sélecteur de couleur
	 */
	$(function(){
	    $('.choix_couleur_bordure').colorpicker().on('changeColor.colorpicker', function(event){
	  		var context = ko.contextFor(this);
	  		var nouvelle_couleur = "rgba("+event.color.toRGB().r+","+event.color.toRGB().g+","+event.color.toRGB().b+","+event.color.toRGB().a+")";
	  		context.$data.bordure.couleur(nouvelle_couleur);
		});
	});

	/**
	 * Formatte la couleur sélectionnée par le sélecteur de couleur au format rgba et l'attribue à 
	 * l'attribut couleur_fond de l'élément
	 * Lancé lors d'un changement de couleur du sélecteur de couleur
	 */
	$(function(){
	    $('.choix_couleur_fond').colorpicker().on('changeColor.colorpicker', function(event){
	  		var context = ko.contextFor(this);
	  		var nouvelle_couleur = "rgba("+event.color.toRGB().r+","+event.color.toRGB().g+","+event.color.toRGB().b+","+event.color.toRGB().a+")";
	  		context.$data.couleur_fond(nouvelle_couleur);
		});
	});
});

/**
 * Attribue la bonne valeur à l'attribut gras du style, selon si le bouton est activé ou non
 * Lancé lors d'un changement de l'élément portant la classe checkbox_gras
 */
$("body").on("change", ".checkbox_gras", function() {
	var context = ko.contextFor(this);
	if (this.checked) {
		context.$data.gras('bold');
	} else {
		context.$data.gras('normal');
	}
});


/**
 * Attribue la bonne valeur à l'attribut italique du style, selon si le bouton est activé ou non
 * Lancé lors d'un changement de l'élément portant la classe checkbox_italique
 */
$("body").on("change", ".checkbox_italique", function() {
	var context = ko.contextFor(this);
	if (this.checked) {
		context.$data.italique('italic');
	} else {
		context.$data.italique('normal');
	}
});

/**
 * Attribue la bonne valeur à l'attribut soulignement du style, selon si le bouton est activé ou non
 * Lancé lors d'un changement de l'élément portant la classe checkbox_soulignement
 */
$("body").on("change", ".checkbox_soulignement", function() {
	var context = ko.contextFor(this);
	if (this.checked) {
		context.$data.soulignement('underline');
	} else {
		context.$data.soulignement('none');
	}
});


/**
 * Fonction qui permet de vérifier si les boutons gras/italique/soulignement doivent être cochés ou non lors
 * de leur initialisation
 */
function verifier_boutons(){
	/**
	 * Vérifie si le bouton gras doit être coché ou non au chargement de la page
	 * Effectué pour tous les éléments portant la classe checkbox_gras
	 */
	$('.checkbox_gras').each(function() {
	    var context = ko.contextFor(this);
		if (context.$data.gras() == 'bold') {
			$(this).prop("checked", true);
			$(this).parent().addClass('active');
		} else {
			$(this).prop("checked", false);
		}
	});

	/**
	 * Vérifie si le bouton italique doit être coché ou non au chargement de la page
	 * Effectué pour tous les éléments portant la classe checkbox_italique
	 */
	$('.checkbox_italique').each(function() {
	    var context = ko.contextFor(this);
		if (context.$data.italique() == 'italic') {
			$(this).prop("checked", true);
			$(this).parent().addClass('active');
		} else {
			$(this).prop("checked", false);
		}
	});

	/**
	 * Vérifie si le bouton soulignement doit être coché ou non au chargement de la page
	 * Effectué pour tous les éléments portant la classe checkbox_soulignement
	 */
	$('.checkbox_soulignement').each(function() {
	    var context = ko.contextFor(this);
		if (context.$data.soulignement() == 'underline') {
			$(this).prop("checked", true);
			$(this).parent().addClass('active');
		} else {
			$(this).prop("checked", false);
		}
	});
}

	/**
	 * Ajoute dynamiquement les polices reçues du serveur dans une balise «style».
	 * NOTE : Ne supporte présentement que les fichiers de type 'ttf'.
	 */
for (i = 0; i < viewModel.polices().length; i++) { 
    $("head").prepend("<style type=\"text/css\">" + 
                                "@font-face {\n" +
                                    "\tfont-family: \""+ viewModel.polices()[i] +"\";\n" + 
                                    "\tsrc: url('../src/" + viewModel.polices()[i] + ".ttf') format('truetype');\n" + 
                                "}\n" + 
                            "</style>");
}

/**
 * Fonction lancée lorsque la page est prête
 */
$(document).ready(function(){


	/**
	 * Formatte la couleur sélectionnée par le sélecteur de couleur au format rgba et l'attribue à 
	 * couleur_fond de la fenêtre
	 * Lancé lors d'un changement de couleur du sélecteur de couleur
	 */
	$(function(){
	    $('.choix_couleur').colorpicker().on('changeColor.colorpicker', function(event){
	  		var nouvelle_couleur = "rgba("+event.color.toRGB().r+","+event.color.toRGB().g+","+event.color.toRGB().b+","+event.color.toRGB().a+")";
	  		viewModel.fenetre.couleur_fond(nouvelle_couleur);
		});
	});


    /**
     * 
     */
    ko.bindingHandlers.selectedIndex = {
        init: function(element, valueAccessor) {
            ko.utils.registerEventHandler(element, "change", function() {
                 var value = valueAccessor();
                if (ko.isWriteableObservable(value)) {
                   value(element.selectedIndex);   
                }
            });
        }
    };

    /**
     * Id de la zone actuellement sélectionnée
     */
    viewModel.id_zone_focus = ko.observable();

    /**
     * @param  {integer} id : id de la zone à vérifier
     * @return {Boolean} : indique si la zone est sélectionnée
     */
    viewModel.is_selected = function (id) {
        return viewModel.fenetre.zones()[viewModel.index_zone_focus()].id() == id;
    };

    /**
     * Affiche ou cache la barre de navigation
     * Lancé par un clic sur un élément portant la classe toggle_sidebar
     */
    $("body").on("click", ".toggle_sidebar", function() {
        $("#sidebar").toggleClass("show_sidebar");
    });

    /**
     * Attribue la zone actuellement sélectionnée
     * Lancé par un clic sur un élément portant la classe zone
     */
    $("body").on("mousedown", ".zone", function() {
        var zone = ko.dataFor(this);
        for (var index in viewModel.fenetre.zones()) {
            if (viewModel.fenetre.zones()[index].id() === zone.id()){
                viewModel.index_zone_focus(parseInt(index));
            }
        }
        viewModel.id_zone_focus(zone.id());
    });
});

/**
 * Sauvegarde les données dans le serveur par un post et rafraîchit la page avec les nouvelles 
 * données
 * @param  {fileName} : 
 */
function appliquer_modifications(fileName) {
    $(window).bind('beforeunload', function(e) {console.log(changes);});
    window.onbeforeunload = null;
    var unmapped = ko.mapping.toJSON(viewModel);
    $.post("/g/" + fileName,
        {
            fileName,
            unmapped
        }
    ).always(function() {
        location.reload();
    });
}

function obtenir_liste_zone_valide() {
    var zones_valides = [];
    for (i = 0; i < viewModel.fenetre.zones().length; i++) { 
        if (viewModel.fenetre.zones()[i].id() >= 0) {
            zones_valides.push(i);
        }
    }
    return zones_valides;
}

if (obtenir_liste_zone_valide().length > 0) {
    viewModel.index_zone_focus = ko.observable(0);
}
else {
    viewModel.index_zone_focus = ko.observable(-1);
}

/**
 * 
 */
function mettre_a_jour_index(index) {
    if (obtenir_liste_zone_valide().length > 0) {
        viewModel.index_zone_focus(index);
    }
    else {
        viewModel.index_zone_focus(-1);
    }
}


/**
 * Déplace l'index correspondant à la zone sélectionné selon la valeur reçue en argument.
 */
function deplacement_index_zone_focus(val) {
    do {
        if (viewModel.index_zone_focus()+val >= viewModel.fenetre.zones().length) {
            viewModel.index_zone_focus(0);
            mettre_a_jour_index(viewModel.index_zone_focus());
        }
        else if (viewModel.index_zone_focus()+val < 0) {
            viewModel.index_zone_focus(viewModel.fenetre.zones().length-1);
            mettre_a_jour_index(viewModel.index_zone_focus());
        }
        else {
            viewModel.index_zone_focus(viewModel.index_zone_focus()+val);
            mettre_a_jour_index(viewModel.index_zone_focus());
        }
    }
    while (viewModel.fenetre.zones()[viewModel.index_zone_focus()].id() <= 0);
}


/**
 * Supprime la zone de la liste des zones de la fenêtre associée en mettant son id négatif si la 
 * zone est enregistrée ou en le retirant directement de la liste si elle a été créée sans être 
 * appliquée
 * Lancé lors d'un clic sur un élément qui porte la classe retirer
 */
$("body").on("click", ".retirer_zone", function() {
    var confirmation = confirm("Êtes-vous sûr de vouloir supprimer " + viewModel.fenetre.zones()[viewModel.index_zone_focus()].nom() +"?");
    if (confirmation) {
        viewModel.fenetre.zones()[viewModel.index_zone_focus()].id(-(viewModel.fenetre.zones()[viewModel.index_zone_focus()].id()));
        deplacement_index_zone_focus(1);
    } else {
        console.log("suppression annulée");
    }
});

/**
 * Supprime la zone de la liste des zones de la fenêtre associée en mettant son id négatif si la 
 * zone est enregistrée ou en le retirant directement de la liste si elle a été créée sans être 
 * appliquée
 * Lancé lors d'un clic sur un élément qui porte la classe bouton_retirer_zone
 */
$("body").on("click", ".bouton_retirer_zone", function() {
    var context = ko.contextFor(this);
    var id = context.$data.id();
    var confirmation = confirm("Êtes-vous sûr de vouloir supprimer " + context.$data.nom() +"?");

    if (confirmation) {            
        context.$data.id(-id);
        deplacement_index_zone_focus(1);
    } else {
        console.log("suppression annulée");
    }
});

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

/**
 * Variable représentant l'image de fond sélectionnée
 */
viewModel.image_fond_focus = ko.observable(viewModel.fenetre.image_fond.id());

/**
 * Attribue les valeurs de l'image de fond sélectionnée à l'image de fond de la fenêtre
 */
viewModel.image_fond_focus.subscribe(function (data) {
    for (var index in viewModel.images()) {
        if (viewModel.images()[index].id() === viewModel.image_fond_focus()){
            viewModel.fenetre.image_fond.id(viewModel.images()[index].id());
            viewModel.fenetre.image_fond.nom(viewModel.images()[index].nom());
            viewModel.fenetre.image_fond.chemin_fichier(viewModel.images()[index].chemin_fichier());
        }
    }
});

/**
 * Variable représentant le thème sélectionné
 */
viewModel.theme_focus = ko.observable(viewModel.fenetre.theme.id());

/**
 * Attribue les valeurs du thème sélectionné au thème de la zone
 */
viewModel.theme_focus.subscribe(function (data) {
    for (var index in viewModel.themes()) {
        if (viewModel.themes()[index].id() === viewModel.theme_focus()){
            viewModel.fenetre.theme.id(viewModel.themes()[index].id());
            viewModel.fenetre.theme.nom(viewModel.themes()[index].nom());
            // titre
            viewModel.fenetre.theme.titre.police(viewModel.themes()[index].titre.police());
            viewModel.fenetre.theme.titre.taille(viewModel.themes()[index].titre.taille());
            viewModel.fenetre.theme.titre.couleur(viewModel.themes()[index].titre.couleur());
            viewModel.fenetre.theme.titre.gras(viewModel.themes()[index].titre.gras());
            viewModel.fenetre.theme.titre.italique(viewModel.themes()[index].titre.italique());
            viewModel.fenetre.theme.titre.soulignement(viewModel.themes()[index].titre.soulignement());

            //sous_titre
            viewModel.fenetre.theme.sous_titre.police(viewModel.themes()[index].sous_titre.police());
            viewModel.fenetre.theme.sous_titre.taille(viewModel.themes()[index].sous_titre.taille());
            viewModel.fenetre.theme.sous_titre.couleur(viewModel.themes()[index].sous_titre.couleur());
            viewModel.fenetre.theme.sous_titre.gras(viewModel.themes()[index].sous_titre.gras());
            viewModel.fenetre.theme.sous_titre.italique(viewModel.themes()[index].sous_titre.italique());
            viewModel.fenetre.theme.sous_titre.soulignement(viewModel.themes()[index].sous_titre.soulignement());
            //texte
            viewModel.fenetre.theme.texte.police(viewModel.themes()[index].texte.police());
            viewModel.fenetre.theme.texte.taille(viewModel.themes()[index].texte.taille());
            viewModel.fenetre.theme.texte.couleur(viewModel.themes()[index].texte.couleur());
            viewModel.fenetre.theme.texte.gras(viewModel.themes()[index].texte.gras());
            viewModel.fenetre.theme.texte.italique(viewModel.themes()[index].texte.italique());
            viewModel.fenetre.theme.texte.soulignement(viewModel.themes()[index].texte.soulignement());
            //tableau
            viewModel.fenetre.theme.tableau.couleur_fond(viewModel.themes()[index].tableau.couleur_fond());
            viewModel.fenetre.theme.tableau.bordure.couleur(viewModel.themes()[index].tableau.bordure.couleur());
            viewModel.fenetre.theme.tableau.bordure.style(viewModel.themes()[index].tableau.bordure.style());
            viewModel.fenetre.theme.tableau.bordure.taille(viewModel.themes()[index].tableau.bordure.taille());
            //tableau_ligne
            viewModel.fenetre.theme.tableau_ligne.bordure.couleur(viewModel.themes()[index].tableau_ligne.bordure.couleur());
            viewModel.fenetre.theme.tableau_ligne.bordure.style(viewModel.themes()[index].tableau_ligne.bordure.style());
            viewModel.fenetre.theme.tableau_ligne.bordure.taille(viewModel.themes()[index].tableau_ligne.bordure.taille());
            //tableau_titre
            viewModel.fenetre.theme.tableau_titre.police(viewModel.themes()[index].tableau_titre.police());
            viewModel.fenetre.theme.tableau_titre.taille(viewModel.themes()[index].tableau_titre.taille());
            viewModel.fenetre.theme.tableau_titre.couleur(viewModel.themes()[index].tableau_titre.couleur());
            viewModel.fenetre.theme.tableau_titre.gras(viewModel.themes()[index].tableau_titre.gras());
            viewModel.fenetre.theme.tableau_titre.italique(viewModel.themes()[index].tableau_titre.italique());
            viewModel.fenetre.theme.tableau_titre.soulignement(viewModel.themes()[index].tableau_titre.soulignement());
            //tableau_sous_titre
            viewModel.fenetre.theme.tableau_sous_titre.police(viewModel.themes()[index].tableau_sous_titre.police());
            viewModel.fenetre.theme.tableau_sous_titre.taille(viewModel.themes()[index].tableau_sous_titre.taille());
            viewModel.fenetre.theme.tableau_sous_titre.couleur(viewModel.themes()[index].tableau_sous_titre.couleur());
            viewModel.fenetre.theme.tableau_sous_titre.gras(viewModel.themes()[index].tableau_sous_titre.gras());
            viewModel.fenetre.theme.tableau_sous_titre.italique(viewModel.themes()[index].tableau_sous_titre.italique());
            viewModel.fenetre.theme.tableau_sous_titre.soulignement(viewModel.themes()[index].tableau_sous_titre.soulignement());
            //tableau_texte
            viewModel.fenetre.theme.tableau_texte.police(viewModel.themes()[index].tableau_texte.police());
            viewModel.fenetre.theme.tableau_texte.taille(viewModel.themes()[index].tableau_texte.taille());
            viewModel.fenetre.theme.tableau_texte.couleur(viewModel.themes()[index].tableau_texte.couleur());
            viewModel.fenetre.theme.tableau_texte.gras(viewModel.themes()[index].tableau_texte.gras());
            viewModel.fenetre.theme.tableau_texte.italique(viewModel.themes()[index].tableau_texte.italique());
            viewModel.fenetre.theme.tableau_texte.soulignement(viewModel.themes()[index].tableau_texte.soulignement());
        }
    }
});


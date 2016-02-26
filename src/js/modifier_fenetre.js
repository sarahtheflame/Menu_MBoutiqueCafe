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
            console.log(nouvelle_couleur);
	  		viewModel.fenetre.couleur_fond(nouvelle_couleur);
		});
	});

	/**
	 * Vérifie le fond d'écran à utiliser (image ou couleur)
	 * @return {[type]}
	 */
	// viewModel.choose_background = ko.computed(function() {
 //        if (viewModel.fenetre.image_fond.chemin_fichier() == "undefined") {
 //            return viewModel.fenetre.couleur_fond();
 //        }
 //        else {
 //            return '../src/' + viewModel.fenetre.image_fond.chemin_fichier();
 //        }
 //    });

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
     * 
     */
    if (viewModel.fenetre.zones().length != 0) {
        viewModel.index_zone_focus = ko.observable(0);
    }
    else {
        viewModel.index_zone_focus = ko.observable(-1);
    }

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
    console.log(unmapped);
    $.post("/g/" + fileName,
        {
            fileName,
            unmapped
        }
    ).always(function() {
        location.reload();
    });
}

/**
 * Sauvegarde les données dans le serveur par un post et rafraîchit la page avec les nouvelles 
 * données
 * @param  {fileName} : 
 */
function deplacement_index_zone_focus(val) {
    console.log(viewModel.index_zone_focus());
    console.log(viewModel.fenetre.zones().length);
    
    if (viewModel.index_zone_focus()+val >= viewModel.fenetre.zones().length) {
        viewModel.index_zone_focus(0);
    }
    else if (viewModel.index_zone_focus()+val <= 0) {
        viewModel.index_zone_focus(viewModel.fenetre.zones().length);
    }
    else {
        viewModel.index_zone_focus(viewModel.index_zone_focus()+val);
    }
}

/**
 * Supprime la zone de la liste des zones de la fenêtre associée en mettant son id négatif si la 
 * zone est enregistrée ou en le retirant directement de la liste si elle a été créée sans être 
 * appliquée
 * Lancé lors d'un clic sur un élément qui porte la classe retirer
 */
$("body").on("click", ".retirer_zone", function() {
    var context = ko.contextFor(this);
    var id = context.$data.id();
    var confirmation = confirm("Êtes-vous sûr de vouloir supprimer " + context.$data.nom() +"?");

    if (confirmation) {
            if (id != 0) {
                context.$data.id(-id);
            } else {
                context.$parent.zones.remove(context.$data);
            }
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


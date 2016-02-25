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


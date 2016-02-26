/**
 * Variable représentant le média sélectionné
 */
viewModel.media_focus = ko.observable(viewModel.zone.image.id());

/**
 * Attribue les valeurs du média sélectionné au média de la zone
 */
viewModel.media_focus.subscribe(function (data) {
    for (var index in viewModel.images()) {
        if (viewModel.images()[index].id() === viewModel.media_focus()){
            viewModel.zone.image.id(viewModel.images()[index].id());
            viewModel.zone.image.nom(viewModel.images()[index].nom());
            viewModel.zone.image.chemin_fichier(viewModel.images()[index].chemin_fichier());
        }
    }
});
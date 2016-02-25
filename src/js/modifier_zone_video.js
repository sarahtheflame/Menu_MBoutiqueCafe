/**
 * Variable représentant le média sélectionné
 */
viewModel.media_focus = ko.observable(viewModel.zone.video.id());

/**
 * Attribue les valeurs du média sélectionné au média de la zone
 */
viewModel.media_focus.subscribe(function (data) {
    for (var index in viewModel.videos()) {
        if (viewModel.videos()[index].id() === viewModel.media_focus()){
            viewModel.zone.video.id(viewModel.videos()[index].id());
            viewModel.zone.video.nom(viewModel.videos()[index].nom());
            viewModel.zone.video.chemin_fichier(viewModel.videos()[index].chemin_fichier());
        }
    }
});
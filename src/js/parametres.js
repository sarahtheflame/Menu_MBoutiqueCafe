/**
 * Modifier les paramètres de l'administrateur connecté selon les valeurs entrées par l'usager
 * Lancé par un clic sur un élément portant la classe modifier_parametres
 */
$("body").on("click", ".modifier_parametres", function() {
    var nouvelle_adresse_courriel = $('#adresse_courriel_input').val();
    var nouveau_mot_de_passe = $('#mot_de_passe_input').val();
    // if ($('#confirmation_mot_de_passe_input').val() === nouveau_mot_de_passe) {
    //     viewModel.administrateur.adresse_courriel(nouvelle_adresse_courriel);
    //     viewModel.administrateur.mot_de_passe(nouveau_mot_de_passe);
    // } 
    viewModel.administrateur.adresse_courriel(nouvelle_adresse_courriel);
    viewModel.administrateur.mot_de_passe(nouveau_mot_de_passe);
});

/**
 * Affiche ou cache le mot de passe
 * Lancé par un clic sur un élément portant la classe toggle_password_2
 */
$("body").on("click", "#toggle_mot_de_passe", function() {
    $('#confirmation_mot_de_passe_input').get(0).type = 'password';
    $('#mot_de_passe_input').get(0).type = 'password';
});
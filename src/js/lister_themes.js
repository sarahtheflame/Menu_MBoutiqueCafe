/**
 * Supprime la période en mettant son id négatif si la zone est enregistrée ou en le retirant
 *  directement de la liste si elle a été créée sans être 
 * appliquée
 * Lancé lors d'un clic sur un élément qui porte la classe retirer
 */
$("body").on("click", ".retirer", function() {
    var context = ko.contextFor(this),
        id = context.$data.id();
    var confirmation = confirm("Êtes-vous sûr de vouloir supprimer " + context.$data.nom() +"?");

    if (confirmation) {
        if (id != 0) {
            context.$data.id(-id);
        } else {
            context.$parent.themes.remove(context.$data);
        }
    } else {
        console.log("suppression annulée");
    }
});

/**
 * Création d'un nouveau thème avec un id à 0 et le nom entré dans le modal
 * Lancé lors d'un clic sur un élément qui porte la classe ajouter_theme
 */
$("body").on("click", ".ajouter_theme", function() {
    var context = ko.contextFor(this);
    var Theme = function(){
        this.id = ko.observable(0);
        this.nom = ko.observable($("#nom_theme_input").val());
    };

    context.$root.themes.push(new Theme());
    $("#nom_theme_input").val('');
    $('[data-toggle="tooltip"]').tooltip({'placement': 'top'});
});


/**
 * Focus sur le champ nom_theme_input lorsque le modal AjouterTheme est affiché
 */
$('body').on('shown.bs.modal', '.modal', function () {
    $('#nom_theme_input').focus();
})
/**
 * Supprime la période en mettant son id négatif si la zone est enregistrée ou en le retirant
 * directement de la liste si elle a été créée sans être 
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
            context.$root.periodes.remove(context.$data);
        }
    } else {
        console.log("suppression annulée");
    }
});
$("body").on("click", ".afficher_periode_actuelle", function() {
    $.post("/afficher_fenetres", {} );
});

/**
 * Création d'une nouvelle période avec un id à 0
 * Lancé lors d'un clic sur un élément qui porte la classe ajouter_periode
 */
$("body").on("click", ".ajouter_periode", function() {
    var context = ko.contextFor(this),
    // Fenetre = function(id){
    //     this.id = ko.observable(id);
    // };

    Periode = function(){
        this.id = ko.observable(0);
        this.nom = ko.observable($("#nom_periode_input").val());
        this.heure_debut = ko.observable($("#heure_debut_input").val());
        this.fenetre_1 = context.$root.fenetres()[0];
        this.fenetre_2 = context.$root.fenetres()[0];
        this.fenetre_3 = context.$root.fenetres()[0];
        this.fenetre_4 = context.$root.fenetres()[0];
    };

    context.$root.periodes.push(new Periode());
    $("#nom_periode_input").val('');
    $('[data-toggle="tooltip"]').tooltip({'placement': 'top'});
});

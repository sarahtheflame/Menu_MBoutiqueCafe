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

/**
 * Création d'une nouvelle période avec un id à 0
 * Lancé lors d'un clic sur un élément qui porte la classe ajouter_periode
 */
$("body").on("click", ".ajouter_periode", function() {
    var context = ko.contextFor(this),
    Fenetre = function(id){
        this.id = ko.observable(id);
    };

    Periode = function(heure_debut){
        alert(heure_debut);
        this.id = ko.observable(0);
        this.heure_debut = ko.observable(heure_debut);
        this.fenetre_1 = ko.observable(new Fenetre(1));
        this.fenetre_2 = ko.observable(new Fenetre(1));
        this.fenetre_3 = ko.observable(new Fenetre(1));
        this.fenetre_4 = ko.observable(new Fenetre(1));
    };

    context.$root.periodes.push(new Periode());
});

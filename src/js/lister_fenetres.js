/**
 * Supprime la zone de la liste des zones de la fenêtre associée en mettant son id négatif si la 
 * zone est enregistrée ou en le retirant directement de la liste si elle a été créée sans être 
 * appliquée
 * Lancé lors d'un clic sur un élément qui porte la classe retirer
 */
$("body").on("click", ".retirer", function() {
    var context = ko.contextFor(this),
        id = context.$data.id();
    if (id != 0) {
        context.$data.id(-id);
    } else {
        context.$parent.zones.remove(context.$data);
    }
});

/**
 * Création d'une nouvelle fenêtre avec un id à 0, le nom entré dans le modal, le thème par défaut 
 * et une liste de zones vides
 * Lancé lors d'un clic sur un élément qui porte la classe ajouter_fenetre
 */
$("body").on("click", ".ajouter_fenetre", function() {
    var context = ko.contextFor(this);
    var Fenetre = function(){
        this.id = ko.observable(0);
        this.nom = ko.observable($("#nom_fenetre_input").val());
        this.theme = ko.observable(context.$root.themes()[0]);
        this.zones = ko.observableArray([]);
    };

    context.$root.fenetres.push(new Fenetre());
    $("#nom_fenetre_input").val('');
    $('[data-toggle="tooltip"]').tooltip({'placement': 'top'});
});

/**
 * Création d'une nouvelle zone dans la liste des zones de la fenêtre associée, avec un id à 0, le 
 * nom entré dans le modal et le type de la zone. Si le type est 'ZoneTable', assigne le nombre de 
 * colonnes choisi dans le modal
 * Lancé lors d'un clic sur un élément qui porte la classe ajouter_zone
 */
$("body").on("click", ".ajouter_zone", function() {
    var context = ko.contextFor(this);
    var Zone = function(){
        this.id = ko.observable(0);
        this.nom = ko.observable($("#nom_zone_input").val());
        this.type = ko.observable($("#choix_type_zone").val());

        if (this.type() === 'ZoneTable') {
            this.nombre_colonnes = ko.observable($("#choix_nb_colonnes").val());
        }
    };
  
    viewModel.fenetre_focus.zones.push(new Zone());
    $("#nom_zone_input").val('');
    $('[data-toggle="tooltip"]').tooltip({'placement': 'top'});
});

/**
 * Focus sur le champ nom_fenetre_input lorsque le modal AjouterFenetre est affiché
 */
$('body').on('shown.bs.modal', '#modalAjouterFenetre', function () {
    $('#nom_fenetre_input').focus();
})

/**
 * Focus sur le champ nom_zone_input lorsque le modal AjouterZone est affiché
 */
$('body').on('shown.bs.modal', '#modalAjouterZone', function () {
    $('#nom_zone_input').focus();
})

/**
 * Variable servant à déterminée la fenêtre choisie lors de la création d'une nouvelle zone
 */
viewModel.fenetre_focus = ko.observable();

/**
 * Attribue la fenêtre focus
 * Lancé lors d'un clic sur un élément portant la classe selecteur_fenetre
 */
$('body').on('click', '.selecteur_fenetre', function () {
    viewModel.fenetre_focus = ko.contextFor(this).$data;
})

/**
 * Liste contenant les choix de types possibles pour une zone. 
 * nom : Nom affiché pour l'utilisateur
 * attribut : Valeur attribuée à l'attribut type de la zone
 */
viewModel.choix_type_zone = ko.observableArray([
    { nom: "Zone Table", attribut: "ZoneTable" },
    { nom: "Zone Image", attribut: "ZoneImage" },
    { nom: "Zone Vidéo", attribut: "ZoneVideo" },
    { nom: "Zone Base", attribut: "ZoneBase" }
]);

/**
 * Variable correspondant au type de zone sélectionné lors de la création d'une nouvelle zone
 */
viewModel.type_zone_focus = ko.observable();
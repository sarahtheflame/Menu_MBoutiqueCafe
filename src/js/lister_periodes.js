$("body").on("click", ".retirer", function() {
    var context = ko.contextFor(this),
        id = context.$data.id();
      if (id != 0) {
        context.$data.id(-id);
      } else {
        context.$parent.zones.remove(context.$data);
      }
});

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

$("body").on("click", ".ajouter_zone", function() {
  var context = ko.contextFor(this),
      nom_zone = prompt("Nom de la nouvelle zone : ", ""),
      type_zone = prompt("Type de la zone : ", "ZoneBase");
  if (nom_zone != null) {
    var Zone = function(nom_zone, type_zone){
      this.id = ko.observable(0);
      this.nom = ko.observable(nom_zone);
      this.type = ko.observable(type_zone);
    };

    context.$data.zones.push(new Zone(nom_zone, type_zone));
  }
});
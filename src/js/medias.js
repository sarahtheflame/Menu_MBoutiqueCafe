$("body").on("click", ".retirer", function() {
  var context = ko.contextFor(this),
      id = context.$data.id();
    if (id != 0) {
      context.$data.id(-id);
    } else {
      context.$parent.zones.remove(context.$data);
    }
});

$("body").on("click", ".ajouter_fenetre", function() {
  var context = ko.contextFor(this);
      var Fenetre = function(){
        this.id = ko.observable(0);
        this.nom = ko.observable($("#nom_fenetre_input").val());
        this.theme = ko.observable(context.$root.themes()[0]);
        this.zones = ko.observableArray([]);
      };

      context.$root.fenetres.push(new Fenetre());
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
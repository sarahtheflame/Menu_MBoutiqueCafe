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

$("body").on("click", ".retirer", function() {
    var context = ko.contextFor(this),
        id = context.$data.id();
    if (id != 0) {
      context.$data.id(-id);
    } else {
      context.$parent.themes.remove(context.$data);
    }
});

$('body').on('shown.bs.modal', '.modal', function () {
  $('#nom_theme_input').focus();
})
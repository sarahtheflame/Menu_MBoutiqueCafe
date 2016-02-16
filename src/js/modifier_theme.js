$(document).ready(function(){
	$('.checkbox_gras').each(function() {
    var context = ko.contextFor(this);
	if (context.$data.gras() == 'bold') {
		$(this).prop("checked", true);
		$(this).parent().addClass('active');
	} else {
		$(this).prop("checked", false);
	}
	});

	console.log("fonction 1");

	$('.checkbox_italique').each(function() {
	    var context = ko.contextFor(this);
		if (context.$data.italique() == 'italic') {
			$(this).prop("checked", true);
			$(this).parent().addClass('active');
		} else {
			$(this).prop("checked", false);
		}
	});

	$('.checkbox_soulignement').each(function() {
	    var context = ko.contextFor(this);
		if (context.$data.soulignement() == 'underline') {
			$(this).prop("checked", true);
			$(this).parent().addClass('active');
		} else {
			$(this).prop("checked", false);
		}
	});

	viewModel.choixStyleBordure = ko.observableArray([
		{ nom: "Solide", attribut: "solid" },
	    { nom: "Pointillée", attribut: "dotted" },
	    { nom: "Aucune", attribut: "none" }
	]);

	$(function(){
    $('.choix_couleur').colorpicker().on('changeColor.colorpicker', function(event){
  		var context = ko.contextFor(this);
  		context.$data.couleur(event.color.toHex());
	});
	});


});

$("body").on("change", ".checkbox_gras", function() {
	var context = ko.contextFor(this);
	if (this.checked) {
		context.$data.gras('bold');
	} else {
		context.$data.gras('normal');
	}
});

$("body").on("change", ".checkbox_italique", function() {
	var context = ko.contextFor(this);
	if (this.checked) {
		context.$data.italique('italic');
	} else {
		context.$data.italique('normal');
	}
	console.log(context.$data.italique());
});

$("body").on("change", ".checkbox_soulignement", function() {
	var context = ko.contextFor(this);
	if (this.checked) {
		context.$data.soulignement('underline');
	} else {
		context.$data.soulignement('none');
	}
	console.log(context.$data.soulignement());
});



$(document).ready(function(){
	$(function(){
	    $('.choix_couleur').colorpicker().on('changeColor.colorpicker', function(event){
	  		var nouvelle_couleur = "rgba("+event.color.toRGB().r+","+event.color.toRGB().g+","+event.color.toRGB().b+","+event.color.toRGB().a+")";
	  		$root.fenetre.couleur_fond(nouvelle_couleur);
		});
	});
});
/**
 * Sauvegarde les données dans le serveur par un post et rafraîchit la page avec les nouvelles 
 * données
 * @param  {fileName} : 
 */
function appliquer_modifications(fileName) {
    $(window).bind('beforeunload', function(e) {console.log(changes);});
    window.onbeforeunload = null;
    var unmapped = ko.mapping.toJSON(viewModel);
    console.log(unmapped);
    $.post("/g/" + fileName,
        {
            fileName,
            unmapped
        }
    ).always(function() {
        location.reload();
    });
}

/**
 * Fonction lancée lorsque la page est prête
 */
$(document).ready(function(){
    /**
     * Affiche ou cache la barre de navigation
     * Lancé lors d'un clic sur un élément portant l'id toggle_sidebar
     */
    $("#toggle_sidebar").click(function(){
        $("#content").toggleClass("show_sidebar");

        var second = $(this).data("secondtext");
        var start = $(this).data("starttext");
        if (second === $(this).text()) {
          $(this).text(start);
        } else {
          $(this).text(second);
        }
    });

    /* ENCORE UTILE? */
    $("body").on("swiperight",function(){
        $("#content").addClass("show_sidebar");
    });
    $("body").on("swipeleft",function(){
        $("#content").removeClass('show_sidebar');
    });
    window.scrollTo(0, 1);

    /**
     * Active les « tooltips » présents sur la page
     */
    $('[data-toggle="tooltip"]').tooltip({'placement': 'top'});

});
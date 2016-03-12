/*
 * Retirer une zone lors de l'évènement de click sur un élément possédant la classe "retirer".
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

/*
 * Téléversement d'une image par requête de type "ajax".
 */
$("#add_image").submit(function (event) {
        event.preventDefault();
        var formData = new FormData($(this)[0]);
        $.ajax({
            url: '/g/televerser',
            type: 'POST',
            data: formData,
            async: false,
            cache: false,
            contentType: false,
            processData: false,
            success: function () {
                location.reload();
            },
            error: function(){
                alert("Une erreur s'est produite!");
                location.reload();
            }
        });
        return false;
});

/*
 * Téléversement d'une vidéo par requête de type "ajax".
 */
$("#add_video").submit(function (event) {
        event.preventDefault();
        var formData = new FormData($(this)[0]);
        $.ajax({
            url: '/g/televerser',
            type: 'POST',
            data: formData,
            async: false,
            cache: false,
            contentType: false,
            processData: false,
            success: function () {
                location.reload();
            },
            error: function(){
                alert("Une erreur s'est produite!");
                location.reload();
            }
        });
        return false;
});

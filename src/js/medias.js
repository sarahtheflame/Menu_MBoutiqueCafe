$("body").on("click", ".retirer", function() {
    var context = ko.contextFor(this),
        id = context.$data.id();
    if (id != 0) {
        context.$data.id(-id);
    } else {
        context.$parent.zones.remove(context.$data);
    }
    console.log(context.$data.id());
});


$("#add_image").submit(function (event) {
    //disable the default form submission
        event.preventDefault();
        //grab all form data  
        var formData = new FormData($(this)[0]);
        formData.append('nom', 'Bonjour');
          console.log(formData);

          var formDataSerialized = $(this).serialize();
          console.log(formDataSerialized);

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
$("#add_video").submit(function (event) {
    //disable the default form submission
        event.preventDefault();
        //grab all form data  
        var formData = new FormData($(this)[0]);
          console.log(formData);

          var formDataSerialized = $(this).serialize();
          console.log(formDataSerialized);

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

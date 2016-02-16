

function appliquer_modifications(fileName) {
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

$(document).ready(function(){
    $("#toggle_sidebar").click(function(){
        $("#content").toggleClass("show_sidebar");
    });
    $("body").on("swiperight",function(){
      $("#content").addClass("show_sidebar");
    });
    $("body").on("swipeleft",function(){
      $("#content").removeClass('show_sidebar');
    });
    window.scrollTo(0, 1);
    $('[data-toggle="tooltip"]').tooltip({'placement': 'top'});
  });
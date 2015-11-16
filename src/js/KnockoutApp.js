$.getJSON( "data.json", function( json ) {
        var data = json;
        var viewModel = ko.mapping.fromJS(data);
        ko.applyBindings(viewModel);
        var unmapped = ko.mapping.toJSON(viewModel);
        console.log(unmapped);
    });

function exportJson() {
    var unmapped = ko.mapping.toJS(viewModel);
    $.post("submit",
            {
              unmapped
            }
        );
}
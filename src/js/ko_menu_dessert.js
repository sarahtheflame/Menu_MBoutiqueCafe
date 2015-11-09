$.getJSON( "src/js/data_dessert.json", function( json ) {
        var data = json;
        var viewModel = ko.mapping.fromJS(data);
        ko.applyBindings(viewModel);
    });
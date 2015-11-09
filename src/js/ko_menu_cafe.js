$.getJSON( "data_cafe.json", function( json ) {
        var data = json;
        var viewModel = ko.mapping.fromJS(data);
        ko.applyBindings(viewModel);
    });
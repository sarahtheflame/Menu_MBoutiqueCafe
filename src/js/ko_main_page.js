var test = {name};
var viewModel = ko.mapping.fromJS(test);
ko.applyBindings(viewModel);

function exportJson(fileName) {
    var vm = ko.dataFor(document.body);
    var unmapped = ko.mapping.toJSON(vm);
    $.post("submit",
            {
                fileName,
                unmapped
            }
        );
}
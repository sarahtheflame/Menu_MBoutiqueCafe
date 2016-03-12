/**
 * Fonction lancée lorsque la page est prête
 */
$(document).ready(function(){
    var changes = 0
	ko.applyBindings(viewModel);
    viewModel.hasChanges = ko.computed(function() {
        ko.toJSON(viewModel);
        changes += 1;
        if (changes > 3){
            changes = 2;
        }
    });
    $(window).bind('beforeunload', function(e) {
        if(changes > 1) {
            return "Vous avez des données non-sauvegardées!";
        }
    });
});


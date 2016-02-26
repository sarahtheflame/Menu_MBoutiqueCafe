/**
 * Fonction lancée lorsque la page est prête
 */
    

   

$(document).ready(function(){
    var changes = 0
    // function unloadPage(){
    //     console.log(changes);
    //     appliquer_modifications('{{!titre}}');
    // }
	ko.applyBindings(viewModel);
     viewModel.hasChanges = ko.computed(function() {
        ko.toJSON(viewModel);
        changes += 1;
        if (changes > 3){
            changes = 2;
        }
    });
    // window.onbeforeunload = unloadPage;
    $(window).bind('beforeunload', function(e) {
        console.log(changes);
        if(changes > 1) {
            return "Vous avez des données non-sauvegardées!";
        }
    });
});


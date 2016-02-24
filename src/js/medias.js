$("body").on("click", ".retirer", function() {
    var context = ko.contextFor(this),
        id = context.$data.id();
    if (id != 0) {
        context.$data.id(-id);
    } else {
        context.$parent.zones.remove(context.$data);
    }
});

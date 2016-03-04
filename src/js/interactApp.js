interact('.zone')
  .draggable({
    inertia: false,
    snap: {
      targets: [
        interact.createSnapGrid({ x: 10, y: 10 })
      ],
      range: Infinity,
      relativePoints: [ { x: 0, y: 0 } ]
    },
    restrict: {
      restriction: "parent",
      endOnly: true,
      elementRect: { top: 0, left: 0, bottom: 1, right: 1 }
    },
    onstart: set_index_zone_focus,
    onmove: dragMoveListener,
    onend: savePosition
  })
  .resizable({
    restrict: {
      restriction: "children",
      endOnly: true,
      elementRect: { left: 1, right: 1, top: 1, bottom: 1 }
    },
    edges: { left: false, right: true, bottom: true, top: false }
  })
  .on('resizemove', function (event) {
    var target = event.target;

    var a_width = (event.rect.width / $(document).width()) *100;
    var a_height = (event.rect.height / $(document).height()) *100;

    viewModel.fenetre.zones()[viewModel.index_zone_focus()].largeur(a_width);
    viewModel.fenetre.zones()[viewModel.index_zone_focus()].hauteur(a_height);

    var table = $(target).children('table')[0];
    // var image = $(target).children('img')[0];
    // var video = $(target).children('video')[0];
    if (typeof table !== 'undefined') {
      var table_width = $(table).width() / $(document).width() *100;
      var table_height = $(table).height() / $(document).height() *100;
      if (a_width < table_width || a_height < table_height) {
        viewModel.fenetre.zones()[viewModel.index_zone_focus()].largeur(table_width);
        viewModel.fenetre.zones()[viewModel.index_zone_focus()].hauteur(table_height);
      }
    }
    // else if (typeof image !== 'undefined') {
    //   var image_width = ($(image).width() / $(document).width()) *100;
    //   var image_height = ($(image).height() / $(document).height()) *100;
    //   if (a_width > image_width || a_height > image_height) {
    //     viewModel.fenetre.zones()[viewModel.index_zone_focus()].largeur(image_width);
    //     viewModel.fenetre.zones()[viewModel.index_zone_focus()].hauteur(image_height);
    //   }
    // }
    // else if (typeof video !== 'undefined') {
    //   var video_width = ($(video).width() / $(document).width()) *100;
    //   var video_height = ($(video).height() / $(document).height()) *100;
    //   if (a_width > video_width || a_height > video_height) {
    //     viewModel.fenetre.zones()[viewModel.index_zone_focus()].largeur(video_width);
    //     viewModel.fenetre.zones()[viewModel.index_zone_focus()].hauteur(video_height);
    //   }
    // }
  });

  function dragMoveListener (event) {
    var target = event.target,
      x = parseFloat(target.style.left) + parseFloat(parseFloat(event.dx / $(document).width()) *100 ),
        y = parseFloat(target.style.top) + parseFloat(parseFloat(event.dy / $(document).height()) *100);

    target.style.left = x + '%';
    target.style.top = y + '%';
  }

  function savePosition (event) {
    var target = event.target,
      x = parseFloat(target.style.left),
        y = parseFloat(target.style.top);
    viewModel.fenetre.zones()[viewModel.index_zone_focus()].position_x(x);
    viewModel.fenetre.zones()[viewModel.index_zone_focus()].position_y(y);
  }

  function set_index_zone_focus (event) {
    console.log("in");
    var zone = ko.dataFor(event.target);
    console.log(zone.nom());
    for (var index in viewModel.fenetre.zones()) {
        if (viewModel.fenetre.zones()[index].id() === zone.id()){
            viewModel.index_zone_focus(parseInt(index));
        }
    }
    viewModel.id_zone_focus(zone.id());
  }
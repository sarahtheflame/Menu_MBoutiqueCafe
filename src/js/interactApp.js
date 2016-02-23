
interact('.zone')
  .draggable({
    inertia: false,
    restrict: {
      restriction: "parent",
      endOnly: true,
      elementRect: { top: 0, left: 0, bottom: 1, right: 1 }
    },
    onmove: dragMoveListener,
    onend: savePosition
  }).on('tap', function (event) {} )
  .resizable({
    restrict: {
      restriction: "children",
      endOnly: true,
      elementRect: { left: 1, right: 1, top: 1, bottom: 1 }
    },
    edges: { left: false, right: true, bottom: true, top: false }
  })
  .on('resizeend', function (event) {
    
  })
  .on('resizemove', function (event) {
    var target = event.target;

    var a_width = event.rect.width / $(document).width() *100;
    var a_height = event.rect.height / $(document).height() *100;

    viewModel.fenetre.zones()[viewModel.index_zone_focus()].largeur(a_width);
    viewModel.fenetre.zones()[viewModel.index_zone_focus()].hauteur(a_height);

    var table = $(target).children('table')[0];
    var image = $(target).children('img')[0];
    if (typeof table !== 'undefined') {
      var table_width = $(table).width() / $(document).width() *100;
      var table_height = $(table).height() / $(document).height() *100;
      if (a_width < table_width || a_height < table_height) {
        viewModel.fenetre.zones()[viewModel.index_zone_focus()].largeur(table_width);
        viewModel.fenetre.zones()[viewModel.index_zone_focus()].hauteur(table_height);
      }
    }
    else if (typeof image !== 'undefined') {
      var image_width = parseFloat(parseFloat($(image).width() / $(document).width()) *100);
      var image_height = parseFloat(parseFloat($(image).height() / $(document).height()) *100);
      if (a_width > image_width || a_height > image_height) {
        viewModel.fenetre.zones()[viewModel.index_zone_focus()].largeur(image_width);
        viewModel.fenetre.zones()[viewModel.index_zone_focus()].hauteur(image_height);
      }
    }
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

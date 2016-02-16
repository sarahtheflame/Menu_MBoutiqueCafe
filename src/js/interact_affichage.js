
interact('.zone')
  .draggable({
    inertia: true,
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
    var target = event.target,
      x = (parseFloat(target.getAttribute('data-x')) || 0),
      y = (parseFloat(target.getAttribute('data-y')) || 0);

    target.style.width  = parseFloat(event.rect.width) + 'px';
    target.style.height = parseFloat(event.rect.height) + 'px';

    console.log(event.rect.width);
    console.log(event.rect.height);

    var table = $(target).children('table')[0];
    var image = $(target).children('img')[0];

    if (typeof table !== 'undefined') {
      if (parseInt(target.style.width) < $(table).width()
              || parseInt(target.style.height) < $(table).height()) {
            target.style.width = $(table).width()+"px";
            target.style.height = $(table).height()+"px";
      }
    }
    if (typeof image !== 'undefined') {
      if (parseInt(target.style.width) > $(image).width()
              || parseInt(target.style.height) > $(image).height()) {
            target.style.width = $(image).width()+"px";
            target.style.height = $(image).height()+"px";
      }
    }
    x += event.deltaRect.left;
    y += event.deltaRect.top;

    target.setAttribute('data-x', x);
    target.setAttribute('data-y', y);
    viewModel.fenetre.zones()[viewModel.zone_focus()-1].largeur(target.style.width);
    viewModel.fenetre.zones()[viewModel.zone_focus()-1].hauteur(target.style.height);
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
    viewModel.fenetre.zones()[viewModel.zone_focus()-1].position_x(x);
    viewModel.fenetre.zones()[viewModel.zone_focus()-1].position_y(y);
  }

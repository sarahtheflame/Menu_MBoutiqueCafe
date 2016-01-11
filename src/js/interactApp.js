
interact('.boite_flottante')
  .draggable({
  
    // enable inertial throwing
    inertia: true,
    // keep the element within the area of it's parent
    restrict: {
      restriction: "parent",
      endOnly: true,
      elementRect: { top: 0, left: 0, bottom: 1, right: 1 }
    },

    // call this function on every dragmove event
    onmove: dragMoveListener,
    // call this function on every dragend event
    onend: savePosition
  })
  .on('tap', function (event) {


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
    var target = event.target,
        x = (parseFloat(target.getAttribute('data-x')) || 0),
        y = (parseFloat(target.getAttribute('data-y')) || 0);

    // update the element's style
    target.style.width  = event.rect.width + 'px';
    target.style.height = event.rect.height + 'px';

    var table = $(target).children('table')[0];
    var image = $(target).children('img')[0];

    if (typeof table !== 'undefined') {
      if (parseInt(target.style.width) < $(table).width()
              || parseInt(target.style.height) < $(table).height()) {

            console.log("NOPE");
            target.style.width = $(table).width()+"px";
            target.style.height = $(table).height()+"px";
      }
    }
    if (typeof image !== 'undefined') {
        console.log("what");
      if (parseInt(target.style.width) > $(image).width()
              || parseInt(target.style.height) > $(image).height()) {

            console.log("NOPE");
            target.style.width = $(image).width()+"px";
            target.style.height = $(image).height()+"px";
      }
    }


    // translate when resizing from top or left edges
    x += event.deltaRect.left;
    y += event.deltaRect.top;

    //target.style.webkitTransform = target.style.transform =
    //    'translate(' + x + 'px,' + y + 'px)';

    target.setAttribute('data-x', x);
    target.setAttribute('data-y', y);
  });

  function dragMoveListener (event) {
    var target = event.target,
        // keep the dragged position in the data-x/data-y attributes
        x = parseFloat(target.style.left) + ((event.dx / $(document).width()) *100 ),
        y = parseFloat(target.style.top) + ((event.dy / $(document).height()) *100);

    // translate the element
    target.style.left = x + '%';
    target.style.top = y + '%';

    // update the posiion attributes
    target.setAttribute('data-x', x);
    target.setAttribute('data-y', y);
  }

  function savePosition (event) {
    var target = event.target
        // keep the dragged position in the data-x/data-y attributes
        // x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx,
        // y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy,
        // x_percent = (($(document).width() / x) *100),
        // y_percent = (($(document).height() / y) *100);

    console.log('stop');
    // target.setAttribute('data-x', x);
  }

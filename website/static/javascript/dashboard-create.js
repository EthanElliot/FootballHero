var showmodal = $('#dashboard-create-showmodal');
var exercisemodal = $('#dashboard-create-exercise-modal');
var hidemodal = $('#dasboard-create-modal-close');


$( showmodal ).on( "click", function(  ) {
    console.log('yes')
    exercisemodal.css('display', 'inline	')
  });


$( hidemodal ).on( "click", function(  ) {
    console.log('yes')
    exercisemodal.css('display', 'none	')
  });
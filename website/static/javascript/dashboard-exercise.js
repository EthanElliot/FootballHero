$('.dashboard-exercise-instructions').hide();


$('#dashboard-exercise-button-instructions').click(function(){
    $('.dashboard-exercise-video').hide();
    $('.dashboard-exercise-instructions').show();

})
$('#dashboard-exercise-button-video').click(function(){
    $('.dashboard-exercise-video').show();
    $('.dashboard-exercise-instructions').hide();
})
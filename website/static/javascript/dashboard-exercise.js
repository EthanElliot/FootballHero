$('.dashboard-exercise-instructions').hide();
$('#dashboard-exercise-button-video').css('background-color', '#0078e7')


$('#dashboard-exercise-button-instructions').click(function(){
    $('.dashboard-exercise-video').hide();
    $('.dashboard-exercise-instructions').show();
    $('#dashboard-exercise-button-instructions').css('background-color', '#0078e7')
    $('#dashboard-exercise-button-video').css('background-color', '#dbdbdb')
    


})
$('#dashboard-exercise-button-video').click(function(){
    $('.dashboard-exercise-video').show();
    $('.dashboard-exercise-instructions').hide();
    $('#dashboard-exercise-button-instructions').css('background-color', '#dbdbdb')
    $('#dashboard-exercise-button-video').css('background-color', '#0078e7')


})
$(document).ready(function(){
    // toggle dishes table
    $('.dishes-btn').click(function(){
        var $dishes = $(this).siblings('table');
        if ($dishes.is('.hidden')) {
            $('span', this).removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
            $dishes.removeClass('hidden');
        } else {
            $('span', this).removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
            $dishes.addClass('hidden');
        }
    });
});

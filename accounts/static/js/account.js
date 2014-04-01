$(document).ready(function(){

    // Toggle the input type between password and text
    $('.eye_conversion').click(function(){
        var $password_input = $('#' + $(this).data('input-id'));
        if ($password_input.attr('type') == 'password') {
            $password_input.attr('type', 'text');
            $(this).removeClass('glyphicon-eye-close').addClass('glyphicon-eye-open');
        } else {
            $password_input.attr('type', 'password');
            $(this).removeClass('glyphicon-eye-open').addClass('glyphicon-eye-close');
        }
    });
});

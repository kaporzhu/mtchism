$(document).ready(function(){
    $.timeliner({});

    // display input weight form
    $('.input-weight-btn').click(function(){
        $(this).siblings('form').toggle();
    });

    // submit weight
    $('.input-weight-form .submit').click(function(){
        var $btn = $(this);
        var $form = $btn.parents('form');
        var weight = parseInt($('.weight', $form).val());
        $.ajax({
            url: $form.data('url'),
            data: {weight: weight},
            success: function(){
                $form.hide();
                $form.siblings('.badge').text(weight + '公斤');
            }
        });
    });

    // display meals
    $('.stage-date').click(function(){
        var id = $(this).attr('for');
        $('#' + id).toggle();
    });
});

$(document).ready(function(){
    // bind datetime picker
    $('input.datetime').datetimepicker();

    // highlight the selected orders
    $('#orders .select-row-btn').change(function(){
        $(this).parents('tr').toggleClass('selected');
    });

    // highlight the all orders
    $('#select-all-btn').change(function(){
        var checked = $(this).is(':checked');
        if (checked) {
            $('table tbody tr input:checkbox:not(:checked)').trigger('click');
        } else {
            $('table tbody tr input:checkbox:checked').trigger('click');
        }
    });

});

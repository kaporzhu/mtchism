$(document).ready(function(){
    // bind datetime picker
    $('input.datetime').datetimepicker();

    // select row handler
    $('#orders .select-row-btn').change(function(){
        $(this).parents('tr').toggleClass('selected');
    });

    // select rows handler
    $('.select-rows-btn').click(function(){
        var type = $(this).data('type');
        select_rows(type);
    });

    // 
    function select_rows(type) {
        if (type == 'all') {
            $('#orders input:checkbox:not(:checked)').trigger('click');
        } else if (type == 'none') {
            $('#orders input:checkbox:checked').trigger('click');
        } else if (type == 'invert') {
            $('#orders input:checkbox').trigger('click');
        }
    }

    // update status button handler
    $('.update-status-btn').click(function(){
        // get selected order ids
        var selected_ids = [];
        $('#orders .select-row-btn:checkbox:checked').each(function(){
            selected_ids.push($(this).data('id'));
        });
        if (selected_ids.length == 0) {
            alert('没有选择任何订单');
            return;
        }

        $.ajax({
            url: $(this).parents('ul').data('update-status-url'),
            dataType: 'json',
            data: {
                ids: selected_ids.join(','),
                status: $(this).data('status')
            },
            success: function(result){
                $('#orders input:checkbox:checked').each(function(){
                    var $status_td = $(this).parents('tr').find('.status');
                    $status_td.text(result.new_status);
                });
                select_rows('none');
            }
        });
    });
});

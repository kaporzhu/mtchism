$(document).ready(function(){
    // add new tag to the tag list
    $('#add-tag-btn').click(function(){
        var new_tag = $('#new-tag-input').val();
        $('#id_tags').prepend($('<option>').attr('value', '-1').text(new_tag));
        $('#new-tag-input').val('');
    });
});

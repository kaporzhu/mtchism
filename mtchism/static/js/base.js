function get_cookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function(){
    // confirm for tag a. Alert confirm message in data-message. If yes, go to the url in data-url.
    $('a.confirm').click(function(){
        if(confirm($(this).data('message'))) {
            window.location.href = $(this).data('url');
        }
    });
});

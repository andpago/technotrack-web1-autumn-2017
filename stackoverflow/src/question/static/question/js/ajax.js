function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function get_csrf_token() {
    return getCookie('csrftoken')
}

function toggle_like(object_id) {
    var btn_id = '#like_question_' + object_id;

    $.ajax({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', get_csrf_token());
        },
        url: '/like/create',
        method: 'POST',
        data: {model_name: 'question', object_id: object_id},
        success: function (result) {
            var btn = $(btn_id);

            if (result === 'on') {
                btn.addClass('btn-warning');
                btn.removeClass('btn-success');
                btn.text('Revoke like');
            } else {
                btn.addClass('btn-success');
                btn.removeClass('btn-warning');
                btn.text('Like');
            }
        }
    });
}

function get_object(type, id) {
    return $.ajax({
        url: '/question/ajax/get/' + type + '/' + id,
        async: false,
    }).responseText;
}

function autoupdate_all() {
    $.each($('.autoupdate'), function (i, obj) {
        var id = $(obj).data('id');
        var type = $(obj).data('type');
        $(obj).html(get_object(type, id));
    });
}

setInterval(autoupdate_all, 5000);

autoupdate_all();
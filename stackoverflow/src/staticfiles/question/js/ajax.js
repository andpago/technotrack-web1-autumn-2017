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

function toggle_like(type, object_id) {
    var btn_id = '#like_' + type + '_' + object_id;

    $.ajax({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', get_csrf_token());
        },
        url: '/like/create',
        method: 'POST',
        data: {model_name: type, object_id: object_id},
        success: function (result) {
            var btn = $(btn_id);

            if (result === 'on') {
                btn.addClass('btn-warning');
                btn.removeClass('btn-success');
                btn.text('Dislike');
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


function get_answer_ids_for_question(question_id) {
    return JSON.parse($.ajax({
        url: '/question/ajax/get/answers_for/' + question_id,
        async: false,
    }).responseText)['ids'];
}

function get_answers_top(n=5) {
    return JSON.parse($.ajax({
        url: '/question/ajax/get/answers_top/' + n,
        async: false,
    }).responseText)['ids'];
}

var answer_ids = {};
// e.g.
// var answer_ids = {
//     9: [1, 2, 3]
// };

function autoupdate_all() {
    $.each($('.autoupdate_container'), function (i, obj) {
        var container = $(obj);

        if (container.data('type') === 'answer') {
            var qid = container.data('question-id');

            if (qid === 'any') {
                if (typeof answer_ids['any'] === 'undefined') {
                    answer_ids['any'] = get_answers_top(5);
                    aids = answer_ids['any'];

                    html = '';

                    for (var id of aids) {
                        html += '<div class="autoupdate" data-type="answer" data-id="' + id + '"></div>';
                    }

                    container.html(html);
                }



            } else if (typeof qid !== 'undefined') {

                var aids = get_answer_ids_for_question(container.data('question-id'));
                var old_ids = new Set(answer_ids[qid]);

                var new_ids = aids.filter(function(x){return !old_ids.has(x);});

                var html = container.html();

                for (var id of new_ids) {
                    html += '<div class="autoupdate" data-type="answer" data-id="' + id + '"></div>';
                }

                answer_ids[qid] = aids;

                container.html(html);
            }
        }
    });

    $.each($('.autoupdate'), function (i, obj) {
        var id = $(obj).data('id');
        var type = $(obj).data('type');
        $(obj).html(get_object(type, id));
    });
}

setInterval(autoupdate_all, 5000);

autoupdate_all();
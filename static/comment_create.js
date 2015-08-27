// Get CSRF from cookie
function getCookie(name) {
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
var csrftoken = getCookie('csrftoken');

// Set CSRF
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


// AJAX for posting
function create_comment() {
    $.ajax({
        url : "", // the endpoint
        type : "POST", // http method
        data : { text : $('#id_text').val(), author_name : $('#id_author_name').val(), root : $('#id_root').val(), parent : $('#id_parent').val(),}, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#id_text').val(''); // remove the value from the input
			$("li#li-"+id).after('<li class="comment level-'+level+'" id="li-'+json.pk+'">\
			<div class="comment-wrapper">\
                <div class="comment-header-author-name">'+json.author_name+'</div>\
				'+json.pk+' <a class="comment-header-anchor-link" href="/desk/tree/'+json.path+'/"> '+json.pub_date+'</a>\
				<div class="comment-content">'+json.text+'</div>\
				<a href="/desk/reply/'+json.pk+'" class="comment-reply-link" data-id="'+json.pk+'"  data-level="'+level+'">Ответить</a>\
				<a href="#" class="comment-cancel-link">Отмена</a>');
        $.getScript("/static/comment_reply.js"); // handle ajax created comment
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

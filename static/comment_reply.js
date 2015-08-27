jQuery(function($) {
    form = $('.comment-form').clone();
	$('.comment-form').hide();
    reply = $('.comment-reply-link');
    cancel = $('.comment-cancel-link');
    cancel.hide();
	reply.show(); // for ajax created comment
	$('.comment-form').remove(); // for ajax created comment
	form.on('submit', function(event){
    event.preventDefault();
    create_comment();
    });


    reply.click(function(e) {
        e.preventDefault();
        reply.show(); // show previous comment's reply link
        cancel.hide(); // hide previous comment's cancel link
        comment = $(this).parents('.comment');
        comment.find(cancel).show();
        $(this).hide();
        $('.comment-form').remove();
        form.clone(true).appendTo(comment);
        $('#id_parent').val($(this).data('id'));
		id = $(this).data('id');
		level = $(this).data('level')+1;
    });

    cancel.click(function(e) {
        e.preventDefault();
        comment = $(this).parents('.comment-wrapper');
        comment.find(reply).show();
        $(this).hide();
        $('.comment-form').remove();
        form.clone(true);
    });
});

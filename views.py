from messag.models import Comment, Root
from messag.forms import AjaxableResponseMixin, CommentForm
from django.views.generic.edit import CreateView

class CommentAdd(AjaxableResponseMixin, CreateView):

    model = Comment
    form_class = CommentForm
    template_name = 'comment_add.html'
    initial={'root': Root.objects.get(id=1)}

    def get_success_url(self):
        return self.kwargs['lnk']
	

# Main message list
class ShowList(AjaxableResponseMixin, CreateView):

    model = Comment
    form_class = CommentForm
    template_name = 'comment_tree.html'
    initial={'root': Root.objects.get(id=1)}
    def get_context_data(self, **kwargs):
        context = super(ShowList, self).get_context_data(**kwargs)
        comment_list = (
            Comment.objects.filter(parent__isnull=True).order_by('-pub_date')
        )
        context['comment_tree'] = comment_list
        return context
		
		
# Comment tree
class ShowTree(ShowList):

    def get_context_data(self, **kwargs):
        context = super(ShowTree, self).get_context_data(**kwargs)
        comment_list = (
            Comment.objects.filter(path__startswith=self.kwargs['comment_id']).order_by('path')
        )
        context['comment_tree'] = comment_list
        return context


def add_user_session_data(instance, form_initial):
    request = instance.request
    data = request.session.get('user_data', {})
    form_initial.update(data)
    return form_initial

	
# If JS disabled
class CommentReply(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_reply_form.html'
    
    def get_initial(self):
        return add_user_session_data(self, {'parent': self.kwargs['parent_id'], 'root': Root.objects.get(id=1)})

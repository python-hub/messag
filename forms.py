from django.forms import ModelForm, widgets
from messag.models import Comment
from django.http import JsonResponse

class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('author_name', 'text', 'parent', 'root')
        widgets = {
            'parent': widgets.HiddenInput,
			'root': widgets.HiddenInput,
        }
        labels = {
            'author_name': 'Ваше имя',
            'text': 'Сообщение',
        }



class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
				'text': self.object.text,
				'author_name': self.object.author_name,
				'parent': self.object.parent.pk,
				'path': self.object.path,
				'pub_date': self.object.pub_date.strftime('%d-%m-%Y %H:%M'),
            }
            return JsonResponse(data)
        else:
            return response

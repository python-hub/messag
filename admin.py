from django.contrib import admin
from messag.models import Comment
from messag.models import Root


class CommentAdmin(admin.ModelAdmin):
	list_display = ('author_name', 'text', 'pub_date',)
	search_fields = ('author_name', 'text',)
	ordering = ('-pub_date',)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Root)

from django.conf.urls import patterns, url

from messag.views import ShowList, ShowTree, CommentAdd, CommentReply

urlpatterns = patterns('',
url(r'^$', ShowList.as_view(), name='index'), 
url(r'^tree/(?P<comment_id>[0-9]+)/$', ShowTree.as_view(), name='tree'),
url(r'^add/from_(?P<lnk>[a-zA-Z0-9/_]+)$', CommentAdd.as_view(), name='comment_add'),
url(r'^reply/(?P<parent_id>[0-9]+)$', CommentReply.as_view(), name='comment_reply'),
)

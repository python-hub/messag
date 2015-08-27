from django.db import models
from datetime import datetime
	
	
class Root(models.Model):
    name=models.CharField(max_length=32)
    seq=models.PositiveSmallIntegerField(default=0)
	
    def __str__(self):
	    return self.name

	
class TreeOrderField(models.CharField):
	def pre_save(self, model_instance, add):
		if add:
			parent=(model_instance.parent or model_instance.root);
			parent.seq+=1;
			parent.save();
			value='%s%04d'%(getattr(parent, self.attname, ''), parent.seq, )[:256]
			setattr(model_instance, self.attname, value)
			return value
		return models.CharField.pre_save(self, model_instance, add)


class Comment(models.Model):
    
	root=models.ForeignKey(Root, null=True)
	parent=models.ForeignKey('self', blank=True, null=True, related_name='child_set')
	author_name=models.CharField(max_length=32)
	text=models.TextField()
	pub_date=models.DateTimeField('date published', default=datetime.now)
	seq=models.PositiveSmallIntegerField(default=0)
	path=TreeOrderField(max_length=256, blank=True)

	@property
	def level(self):
		return max(0,len(self.path)/4-1)

	class Admin:
		list_display=('pub_date', 'author_name', )
		search_fields=('text', )
		list_filter=('author_name', )
		date_hierarchy='pub_date'
		fields=(
			('Author', {'fields':('author_name', )}),
			('Comment', {'fields':('text', 'pub_date', )}),
			('Advanced', {'fields':('parent', 'path', ), 'classes': 'collapse'}),
		)

	def __str__(self):
		return '%s, "%s"' % (self.author_name, self.text[0:50])
		
	def get_absolute_url(self):
		return '/desk/tree/{}/#comment-{}'.format(self.path, self.id)

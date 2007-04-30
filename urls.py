from django.conf.urls.defaults import *
from djangoforum.models import Forum

forum_dict = {
	'queryset' : Forum.objects.all(),
}

urlpatterns = patterns('',
	(r'^$', 'django.views.generic.list_detail.object_list', forum_dict),
	(r'^(?P<slug>[A-Za-z0-9-_]+)/$', 'djangoforum.views.forum'),
	(r'^(?P<forum>[A-Za-z0-9-_]+)/(?P<thread>[0-9]+)/$', 'djangoforum.views.thread'),
	(r'^(?P<forum>[A-Za-z0-9-_]+)/(?P<thread>[0-9]+)/reply/$', 'djangoforum.views.reply'),
)

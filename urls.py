"""
URLConf for Django-Forum.

django-forum assumes that the forum application is living under
/forum/.

Usage in your base urls.py:
    (r'^forum/', include('forum.urls')),

"""

from django.conf.urls.defaults import *
from forum.models import Forum

forum_dict = {
    'queryset' : Forum.objects.filter(parent__isnull=True),
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', forum_dict),

    (r'^thread/(?P<thread>[0-9]+)/$', 'forum.views.thread'),
    (r'^thread/(?P<thread>[0-9]+)/reply/$', 'forum.views.reply'),

    (r'^(?P<slug>[-\w]+)/$', 'forum.views.forum'),
    (r'^(?P<forum>[-\w]+)/new/$', 'forum.views.newthread'),

    (r'^([-\w/]+/)(?P<forum>[-\w]+)/new/$', 'forum.views.newthread'),
    (r'^([-\w/]+/)(?P<slug>[-\w]+)/$', 'forum.views.forum'),
)

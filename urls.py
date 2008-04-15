"""
URLConf for Django-Forum.

django-forum assumes that the forum application is living under
/forum/.

Usage in your base urls.py:
    (r'^forum/', include('forum.urls')),

"""

from django.conf.urls.defaults import *
from forum.models import Forum
from forum.feeds import RssForumFeed, AtomForumFeed

forum_dict = {
    'queryset' : Forum.objects.filter(parent__isnull=True),
}

feed_dict = {
    'rss' : RssForumFeed,
    'atom': AtomForumFeed
}

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.list_detail.object_list', forum_dict, name='forum_index'),
    
    url(r'^(?P<url>(rss|atom).*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feed_dict}),

    url(r'^thread/(?P<thread>[0-9]+)/$', 'forum.views.thread', name='forum_view_thread'),
    url(r'^thread/(?P<thread>[0-9]+)/reply/$', 'forum.views.reply', name='forum_reply_thread'),

    url(r'^subscriptions/$', 'forum.views.updatesubs', name='forum_subscriptions'),

    url(r'^(?P<slug>[-\w]+)/$', 'forum.views.forum', name='forum_thread_list'),
    url(r'^(?P<forum>[-\w]+)/new/$', 'forum.views.newthread', name='forum_new_thread'),

    url(r'^([-\w/]+/)(?P<forum>[-\w]+)/new/$', 'forum.views.newthread'),
    url(r'^([-\w/]+/)(?P<slug>[-\w]+)/$', 'forum.views.forum', name='forum_subforum_thread_list'),
)

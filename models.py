""" 
A basic forum model with corresponding thread/post models.

Just about all logic required for smooth updates is in the save() 
methods. A little extra logic is in views.py.
"""

from django.db import models
import datetime
from django.contrib.auth.models import User
from django.conf import settings

class Forum(models.Model):
    """
    Very basic outline for a Forum, or group of threads. The threads
    and posts fielsd are updated by the save() methods of their
    respective models and are used for display purposes.

    All of the parent/child recursion code here is borrowed directly from
    the Satchmo project: http://www.satchmoproject.com/
    """
    title = models.CharField(maxlength=100)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child')
    description = models.TextField()
    threads = models.IntegerField(default=0)
    posts = models.IntegerField(default=0)
    forum_latest_post = models.ForeignKey('Post', blank=True, null=True, related_name='forum_latest_post')

    def _recurse_for_parents_slug(self, forum_obj):
        #This is used for the urls
        p_list = []
        if forum_obj.parent_id:
            p = forum_obj.parent
            p_list.append(p.slug)
            more = self._recurse_for_parents_slug(p)
            p_list.extend(more)
        if forum_obj == self and p_list:
            p_list.reverse()
        return p_list

    class Admin:
        list_display = ('title', '_parents_repr')
        ordering = ['parent', 'title']

    def get_absolute_url(self):
        p_list = self._recurse_for_parents_slug(self)
        p_list.append(self.slug)
        return '%s/%s/' % (settings.FORUM_BASE, '/'.join (p_list))

    def _recurse_for_parents_name(self, forum_obj):
        #This is used for the visual display & save validation
        p_list = []
        if forum_obj.parent_id:
            p = forum_obj.parent
            p_list.append(p.title)
            more = self._recurse_for_parents_name(p)
            p_list.extend(more)
        if forum_obj == self and p_list:
            p_list.reverse()
        return p_list

    def get_separator(self):
        return ' &raquo; '

    def _parents_repr(self):
        p_list = self._recurse_for_parents_name(self)
        return self.get_separator().join(p_list)
    _parents_repr.short_description = _("Forum parents")

    def _recurse_for_parents_name_url(self, forum__obj):
        #Get all the absolute urls and names (for use in site navigation)
        p_list = []
        url_list = []
        if forum__obj.parent_id:
            p = forum__obj.parent
            p_list.append(p.title)
            url_list.append(p.get_absolute_url())
            more, url = self._recurse_for_parents_name_url(p)
            p_list.extend(more)
            url_list.extend(url)
        if forum__obj == self and p_list:
            p_list.reverse()
            url_list.reverse()
        return p_list, url_list

    def get_url_name(self):
        #Get a list of the url to display and the actual urls
        p_list, url_list = self._recurse_for_parents_name_url(self)
        p_list.append(self.title)
        url_list.append(self.get_absolute_url())
        return zip(p_list, url_list)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title',]

    def save(self):
        p_list = self._recurse_for_parents_name(self)
        if (self.title) in p_list:
            raise validators.ValidationError(_("You must not save a forum in itself!"))
        super(Forum, self).save()

    def _flatten(self, L):
        """
        Taken from a python newsgroup post
        """
        if type(L) != type([]): return [L]
        if L == []: return L
        return self._flatten(L[0]) + self._flatten(L[1:])

    def _recurse_for_children(self, node):
        children = []
        children.append(node)
        for child in node.child.all():
            children_list = self._recurse_for_children(child)
            children.append(children_list)
        return(children)

    def get_all_children(self):
        """
        Gets a list of all of the children forums.
        """
        children_list = self._recurse_for_children(self)
        flat_list = self._flatten(children_list[1:])
        return(flat_list)

class Thread(models.Model):
    """
    A Thread belongs in a Forum, and is a collection of posts.

    Threads can be closed or stickied which alter their behaviour 
    in the thread listings. Again, the posts & views fields are 
    automatically updated with saving a post or viewing the thread.
    """
    forum = models.ForeignKey(Forum)
    title = models.CharField(maxlength=100)
    sticky = models.BooleanField(blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    posts = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    thread_latest_post = models.ForeignKey('Post', blank=True, null=True, related_name='thread_latest_post')

    class Meta:
        ordering = ('-sticky', '-thread_latest_post')

    def save(self):
        if not self.id:
            f = Forum.objects.get(id=self.forum.id)
            f.threads += 1
            f.save()
        super(Thread, self).save()
    
    def get_absolute_url(self):
        return '%s/thread/%s/' % (settings.FORUM_BASE, self.id)
    
    class Admin:
        pass

    def __str__(self):
        return self.title

class Post(models.Model):
    """ 
    A Post is a User's input to a thread. Uber-basic - the save() 
    method also updates models further up the heirarchy (Thread,Forum)
    """
    thread = models.ForeignKey(Thread)
    author = models.ForeignKey(User)
    body = models.TextField()
    time = models.DateTimeField(blank=True, null=True)

    def save(self):
        new_post = False
        if not self.id:
            self.time = datetime.datetime.now()
            new_post = True
            
        super(Post, self).save()

        if new_post:
            t = Thread.objects.get(id=self.thread.id)
            t.thread_latest_post_id = self.id
            t.posts += 1
            t.save()

            f = Forum.objects.get(id=self.thread.forum.id)
            f.forum_latest_post_id = self.id
            f.posts += 1
            f.save()

    class Meta:
        ordering = ('-time',)
        
    def get_absolute_url(self):
        return '%s#post%s' % (self.thread.get_absolute_url(), self.id)
    
    class Admin:
        pass

    def __str__(self):
        return "%s" % self.id

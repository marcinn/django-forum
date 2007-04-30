from django.db import models
import datetime
from django.contrib.auth.models import User

class Forum(models.Model):
	title = models.CharField(maxlength=100)
	slug = models.SlugField()
	description = models.TextField()
	threads = models.IntegerField(default=0)
	posts = models.IntegerField(default=0)
	forum_latest_post = models.ForeignKey('Post', blank=True, null=True, related_name='forum_latest_post')

	class Admin:
		pass

	def get_absolute_url(self):
		return '/forum/%s/' % self.slug

	def __str__(self):
		return self.title

class Thread(models.Model):
	forum = models.ForeignKey(Forum)
	title = models.CharField(maxlength=100)
	sticky = models.BooleanField(blank=True, null=True)
	closed = models.BooleanField(blank=True, null=True)
	posts = models.IntegerField(default=0)
	views = models.IntegerField(default=0)
	thread_latest_post = models.ForeignKey('Post', blank=True, null=True, related_name='thread_latest_post')

	class Meta:
		ordering = ('sticky', '-thread_latest_post')

	def save(self):
		if not self.id:
			f = Forum.objects.get(id=self.forum.id)
			f.threads += 1
			f.save()
		super(Thread, self).save()
	
	def get_absolute_url(self):
		return '/forum/%s/%s/' % (self.forum.slug, self.id)
	
	class Admin:
		pass

	def __str__(self):
		return self.title

class Post(models.Model):
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
		return '/forum/%s/%s/#post%s' % (self.thread.forum.slug, self.thread.id, self.id)
	
	class Admin:
		pass

	def __str__(self):
		return "%s" % self.id
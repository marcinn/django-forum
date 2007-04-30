from djangoforum.models import Forum,Thread,Post
from datetime import datetime
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext

def forum(request, slug):
	f = get_object_or_404(Forum, slug=slug)
	threads = f.thread_set.all()

	return render_to_response('djangoforum/thread_list.html',
		RequestContext(request, {
			'forum': f,
			'threads': threads,
		}))

def thread(request, forum, thread):
	f = get_object_or_404(Forum, slug=forum)
	t = get_object_or_404(Thread, pk=thread)
	p = t.post_set.all().order_by('time')
	
	return render_to_response('djangoforum/thread.html',
		RequestContext(request, {
			'forum': f,
			'thread': t,
			'posts': p,
		}))

def reply(request, forum, thread):
	f = get_object_or_404(Forum, slug=forum)
	t = get_object_or_404(Thread, pk=thread)
	body = request.POST.get('body', False)
	p = Post(
		thread=t, 
		author=request.user,
		body=body,
		time=datetime.now(),
		)
	p.save()
	return HttpResponseRedirect(p.get_absolute_url())

"""
All forum logic is kept here - displaying lists of forums, threads 
and posts, adding new threads, and adding replies.
"""

from forum.models import Forum,Thread,Post,Subscription
from datetime import datetime
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden
from django.template import RequestContext, Context, loader
from django import newforms as forms
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.defaultfilters import striptags, wordwrap
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

def forum(request, slug):
    """
    Displays a list of threads within a forum.
    Threads are sorted by their sticky flag, followed by their 
    most recent post.
    """
    f = get_object_or_404(Forum, slug=slug)

    return render_to_response('forum/thread_list.html',
        RequestContext(request, {
            'forum': f,
            'threads': f.thread_set.all()
        }))

def thread(request, thread):
    """
    Increments the viewed count on a thread then displays the 
    posts for that thread, in chronological order.
    """
    t = get_object_or_404(Thread, pk=thread)
    p = t.post_set.all().order_by('time')
    s = t.subscription_set.filter(author=request.user)

    t.views += 1
    t.save()
    
    return render_to_response('forum/thread.html',
        RequestContext(request, {
            'forum': t.forum,
            'thread': t,
            'posts': p,
            'subscription': s,
        }))

def reply(request, thread):
    """
    If a thread isn't closed, and the user is logged in, post a reply
    to a thread. Note we don't have "nested" replies at this stage.
    """
    if not request.user.is_authenticated():
        return HttpResponseServerError()
    t = get_object_or_404(Thread, pk=thread)
    if t.closed:
        return HttpResponseServerError()
    body = request.POST.get('body', False)
    p = Post(
        thread=t, 
        author=request.user,
        body=body,
        time=datetime.now(),
        )
    p.save()

    sub = Subscription.objects.filter(thread=t, author=request.user)
    if request.POST.get('subscribe',False):
        if not sub:
            s = Subscription(
                author=request.user,
                thread=t
                )
            s.save()
    else:
        if sub:
            sub.delete()

    # Subscriptions are updated now send mail to all the authors subscribed in
    # this thread.
    mail_subject = ''
    try:
        mail_subject = settings.FORUM_MAIL_PREFIX 
    except AttributeError:
        mail_subject = '[Forum]'

    mail_from = ''
    try:
        mail_from = settings.FORUM_MAIL_FROM
    except AttributeError:
        mail_from = settings.DEFAULT_FROM_EMAIL

    mail_tpl = loader.get_template('forum/notify.txt')
    c = Context({
        'body': wordwrap(striptags(body), 72),
        'site' : Site.objects.get_current(),
        'thread': t,
        })

    #email = EmailMessage('Hello', 'Body goes here', 'from@example.com',
    #            ['to1@example.com', 'to2@example.com'], ['bcc@example.com'],
    #                        headers = {'Reply-To': 'another@example.com'})
    email = EmailMessage(
            subject=mail_subject+' '+striptags(t.title),
            body= mail_tpl.render(c),
            from_email=mail_from,
            to=[mail_from],
            bcc=[s.author.email for s in t.subscription_set.all()],)
    email.send(fail_silently=True)

    return HttpResponseRedirect(p.get_absolute_url())

def newthread(request, forum):
    """
    Rudimentary post function - this should probably use 
    newforms, although not sure how that goes when we're updating 
    two models.

    Only allows a user to post if they're logged in.
    """
    if not request.user.is_authenticated():
        return HttpResponseServerError()
    f = get_object_or_404(Forum, slug=forum)
    t = Thread(
        forum=f,
        title=request.POST.get('title'),
    )
    t.save()
    p = Post(
        thread=t,
        author=request.user,
        body=request.POST.get('body'),
        time=datetime.now(),
    )
    p.save()
    if request.POST.get('subscribe',False):
        s = Subscription(
            author=request.user,
            thread=t
            )
        s.save()
    return HttpResponseRedirect(t.get_absolute_url())

def updatesubs(request):
    """
    Allow users to update their subscriptions all in one shot.
    """
    if not request.user.is_authenticated():
        return HttpResponseForbidden('Sorry, you need to login.')

    subs = Subscription.objects.filter(author=request.user)

    if request.POST:
        # remove the subscriptions that haven't been checked.
        post_keys = [k for k in request.POST.keys()]
        for s in subs:
            if not str(s.thread.id) in post_keys:
                s.delete()
        return HttpResponseRedirect(reverse('forumsubs'))

    return render_to_response('forum/updatesubs.html',
        RequestContext(request, {
            'subs': subs,
        }))
       

============
Django Forum
============

This is a very basic forum application that can plug into any
existing Django installation and use it's existing templates,
users, and admin interface. 

It's perfect for adding forum functionality to an existing website.

Development was done on Django SVN rev. 5007. YMMV on other revisions.

Please send comments/suggestions to me directly, ross at rossp dot org.

Google Code Page / SVN: http://code.google.com/p/django-forum/
My Home Page: http://www.rossp.org

Current Status
--------------

 * It's very basic in terms of features, but it works and is usable.
 * Uses Django Admin for maintenance / moderation - no in-line admin.
 * Uses existing django Auth and assumes you already have that up and
   running. I use and recommend django-registration [1]
 * Roll your own site with little work: Install Django, install
   django-registration, flatpages, django-forum, setup your templates
   and you have an instant website :)
 * Code is as pulled out of my other projects - changes will be made as I
   go to make sure it's as standalone as possible, right now should be
   pretty good.

[1] http://code.google.com/p/django-registration/

Getting Started
---------------

   1. Checkout code via SVN into your python path.
       svn co http://django-forum.googlecode.com/svn/trunk/ forum
   3. Add 'forum' to your INSTALLED_APPS in settings.py
   4. ./manage.py syncdb
   5. Add FORUM_BASE='/forum' to your settings.py (no trailing slash)
   6. Update urls.py: (r'^forum/', include('forum.urls')),
   7. Go to your site admin, add a forum
   8. Browse to yoursite.com/forum/
   9. Enjoy :)

Note: You can change FORUM_BASE to any URI you like, as long as it has a 
leading slash and no trailing slash. Just update urls.py to match.

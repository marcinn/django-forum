
from south.db import db
from django.db import models
from forum.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Forum'
        db.create_table('forum_forum', (
            ('id', orm['forum.Forum:id']),
            ('title', orm['forum.Forum:title']),
            ('slug', orm['forum.Forum:slug']),
            ('parent', orm['forum.Forum:parent']),
            ('description', orm['forum.Forum:description']),
            ('threads', orm['forum.Forum:threads']),
            ('posts', orm['forum.Forum:posts']),
            ('ordering', orm['forum.Forum:ordering']),
        ))
        db.send_create_signal('forum', ['Forum'])
        
        # Adding model 'Post'
        db.create_table('forum_post', (
            ('id', orm['forum.Post:id']),
            ('thread', orm['forum.Post:thread']),
            ('author', orm['forum.Post:author']),
            ('body', orm['forum.Post:body']),
            ('body_html', orm['forum.Post:body_html']),
            ('time', orm['forum.Post:time']),
        ))
        db.send_create_signal('forum', ['Post'])
        
        # Adding model 'Subscription'
        db.create_table('forum_subscription', (
            ('id', orm['forum.Subscription:id']),
            ('author', orm['forum.Subscription:author']),
            ('thread', orm['forum.Subscription:thread']),
        ))
        db.send_create_signal('forum', ['Subscription'])
        
        # Adding model 'Thread'
        db.create_table('forum_thread', (
            ('id', orm['forum.Thread:id']),
            ('forum', orm['forum.Thread:forum']),
            ('title', orm['forum.Thread:title']),
            ('sticky', orm['forum.Thread:sticky']),
            ('closed', orm['forum.Thread:closed']),
            ('posts', orm['forum.Thread:posts']),
            ('views', orm['forum.Thread:views']),
            ('latest_post_time', orm['forum.Thread:latest_post_time']),
        ))
        db.send_create_signal('forum', ['Thread'])
        
        # Adding ManyToManyField 'Forum.groups'
        db.create_table('forum_forum_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('forum', models.ForeignKey(orm.Forum, null=False)),
            ('group', models.ForeignKey(orm['auth.Group'], null=False))
        ))
        
        # Creating unique_together for [author, thread] on Subscription.
        db.create_unique('forum_subscription', ['author_id', 'thread_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [author, thread] on Subscription.
        db.delete_unique('forum_subscription', ['author_id', 'thread_id'])
        
        # Deleting model 'Forum'
        db.delete_table('forum_forum')
        
        # Deleting model 'Post'
        db.delete_table('forum_post')
        
        # Deleting model 'Subscription'
        db.delete_table('forum_subscription')
        
        # Deleting model 'Thread'
        db.delete_table('forum_thread')
        
        # Dropping ManyToManyField 'Forum.groups'
        db.delete_table('forum_forum_groups')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'forum.forum': {
            'description': ('django.db.models.fields.TextField', [], {}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'to': "orm['forum.Forum']"}),
            'posts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'threads': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'forum.post': {
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forum_post_set'", 'to': "orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'body_html': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Thread']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'forum.subscription': {
            'Meta': {'unique_together': "(('author', 'thread'),)"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Thread']"})
        },
        'forum.thread': {
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Forum']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_post_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'posts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }
    
    complete_apps = ['forum']

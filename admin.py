from django.contrib import admin
from forum.models import Forum, Thread, Post, Subscription

class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', '_parents_repr')
    ordering = ['parent', 'title']

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['author','thread']

admin.site.register(Forum, ForumAdmin)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Subscription, SubscriptionAdmin)

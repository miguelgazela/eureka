from django.contrib import admin
from ideas.models import Idea, Comment, Interest, Like

class IdeaAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'text', 'state', 'created', 'updated')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'idea', 'text', 'created')

admin.site.register(Idea, IdeaAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Interest)
admin.site.register(Like)
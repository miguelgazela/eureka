from django.contrib import admin
from ideas.models import Idea, Comment, Vote, Interest

class IdeaAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'text', 'state', 'created', 'updated')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'idea', 'text', 'created')

admin.site.register(Idea, IdeaAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Vote)
admin.site.register(Interest)
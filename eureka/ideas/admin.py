from django.contrib import admin
from ideas.models import Idea, Comment, Vote, Interest

class IdeaAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'text', 'state', 'created', 'updated')

admin.site.register(Idea, IdeaAdmin)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Interest)
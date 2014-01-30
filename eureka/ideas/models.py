from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager

import datetime

# Create your models here.

class Idea(models.Model):
    STATE_CHOICES = (
        ('A', 'Approved'),
        ('R', 'Rejected'),
        ('I', 'Idle'),
    )

    user = models.ForeignKey(User)
    title = models.CharField(max_length=160)
    text = models.TextField()
    # A - approved; R - rejected; I - idle
    state = models.CharField(max_length=1, choices=STATE_CHOICES,default='I')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    def __unicode__(self):
        return "{user.username}: {title}".format(
            user=self.user, title=self.title)

    def was_added_recently(self):
        """
        returns true if the idea was added in the last 3 days
        """
        return self.created >= timezone.now() - datetime.timedelta(days=3);

    def was_edited(self):
        return (self.updated - self.created) > datetime.timedelta(seconds=1)


class Comment(models.Model):
    user = models.ForeignKey(User)
    idea = models.ForeignKey(Idea)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s said %s" % (self.user.username, self.text[:160])

    def was_edited(self):
        return (self.updated - self.created) > datetime.timedelta(seconds=1)


class Vote(models.Model):
    VOTE_CHOICES = (
        ('U', 'Like'),
        ('D', 'Dislike'),
        ('N', 'None'),
    )

    user = models.OneToOneField(User)
    idea = models.OneToOneField(Idea)
    kind = models.CharField(max_length=1, choices=VOTE_CHOICES, default='N')

    def __unicode__(self):
        return "%s voted on %s" % (self.user.username, self.idea.title)


class Interest(models.Model):
    user = models.ForeignKey(User)
    idea = models.ForeignKey(Idea)
    created = models.DateTimeField(auto_now_add=True, default=timezone.now())

    def __unicode__(self):
        return "%s is interested in %s" % (self.user.username, self.idea.title)

from django.conf.urls import patterns, include, url
from ideas import views
import notifications

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^help$', views.help, name="help"),
    url(r'^inbox/notifications/', include(notifications.urls)),

    # auth urls
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^signup$', views.signup, name="signup"),

    # ideas urls
    url(r'^ideas$', views.ideas, name="ideas"),
    url(r'^ideas/(?P<sort>[a-z]{1,})/$', views.ideas, name="ideas"),
    url(r'^ideas/add$', views.add_idea, name="add_idea"),
    url(r'^ideas/(?P<idea_id>\d+)$', views.idea, name="idea"),
    url(r'^ideas/edit/(?P<idea_id>\d+)$', views.edit_idea, name='edit_idea'),

    # users
    url(r'^users$', views.users, name="users"),
    url(r'^users/(?P<sort>[a-z]{1,})/$', views.users, name="users"),
    url(r'^users/(?P<user_id>\d+)$', views.user, name="user"),
    # url(r'^users/(?P<username>[a-zA-Z0-9@.+-_]{1})$', views.user, name="user"),
    url(r'^users/(?P<user_id>\d+)/(?P<tab>[a-z]{1,})/$', views.user, name="user"),
    url(r'^users/edit$', views.edit_user, name="edit_user"),

    # search
    url(r'^search$', views.search, name="search"),

    # api
    url(r'^api/ideas/delete/(?P<idea_id>\d+)$', views.delete_idea, name="delete_idea"),
    url(r'^api/interest/(?P<idea_id>\d+)$', views.add_interest, name='add_interest'),
    url(r'^api/interest/remove/(?P<idea_id>\d+)$', views.remove_interest, name='remove_interest'),
    url(r'^api/comments/(?P<idea_id>\d+)$', views.add_comment, name="add_comment"),
    url(r'^api/comments/delete/(?P<comment_id>\d+)$', views.delete_comment, name="delete_comment"),
    url(r'^api/comments/edit/(?P<comment_id>\d+)$', views.edit_comment, name="edit_comment"),
    url(r'^api/ideas/like/(?P<idea_id>\d+)$', views.like, name="like"),
    url(r'^api/ideas/dislike/(?P<idea_id>\d+)$', views.dislike, name="dislike"),
    url(r'^api/ideas/state/(?P<idea_id>\d+)/(?P<state>[ARI]{1})$', views.change_state, name="change_state"),
    url(r'^api/tags$', views.tags, name="tags"),
    url(r'^api/notifications/mark_all_as_read$', views.notify_mark_all_as_read, name="mark_all_as_read"),
)

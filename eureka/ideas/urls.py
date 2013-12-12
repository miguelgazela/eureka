from django.conf.urls import patterns, include, url
from ideas import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^signup$', views.signup, name="signup"),
    url(r'^ideas$', views.ideas, name="ideas"),
    url(r'^ideas/add$', views.add_idea, name="add_idea"),
    url(r'^ideas/(?P<idea_id>\d+)$', views.idea, name="idea")
)

from django.conf.urls import patterns, include, url
from ideas import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^signup$', views.signup, name="signup"),
)

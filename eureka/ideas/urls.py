from django.conf.urls import patterns, include, url
from ideas import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name="login"),
)

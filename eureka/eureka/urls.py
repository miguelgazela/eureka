from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eureka.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include('ideas.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^app/', include('ideas.urls')),    
)

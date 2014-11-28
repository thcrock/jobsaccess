from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jobsaccess.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'transitfuture.views.jobs', name='jobs'),
    url(r'^blocks.json', 'transitfuture.views.allblocks', name='allblocks'),
    url(r'^blocks', 'transitfuture.views.blockspage', name='blockspage'),
)

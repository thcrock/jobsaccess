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
    url(r'^otpresults', 'transitfuture.views.otpresultspage'),
    url(r'^otp.json', 'transitfuture.views.otpresults'),
    url(r'^bikesheds$', 'transitfuture.views.bikeshedspage'),
    url(r'^bikeshed.json', 'transitfuture.views.bikeshed'),
    url(r'^tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+)/(?P<lookup_key>.+)', 'transitfuture.views.tile'),
)

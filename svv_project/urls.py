from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from svv.views import PodcastListView, PodcastDetailView, PodcastFeed

urlpatterns = patterns('',
    url(r'^$', PodcastListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', PodcastDetailView.as_view(), name='detail'),
    url(r'^feed/$', PodcastFeed(), name='feed'),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

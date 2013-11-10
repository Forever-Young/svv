from django.contrib.syndication.views import Feed
from django.views.generic import ListView, DetailView

from svv.models import PodcastIssue


class PodcastFeed(Feed):
    title = "SiliconValleyVoice"
    link = "https://www.youtube.com/user/SiliconValleyVoice/videos"
    description = "SiliconValleyVoice MP3 files."
    author_name = "Mikhail Portnov"
    item_enclosure_mime_type = "audio/mpeg"

    def items(self):
        return PodcastIssue.objects.exclude(title__isnull=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.short_description

    def item_enclosure_url(self, item):
        return item.file.url

    def item_enclosure_length(self, item):
        return item.file.size

    def item_pubdate(self, item):
        return item.pub_date


class PodcastListView(ListView):
    paginate_by = 6
    queryset = PodcastIssue.objects.exclude(title__isnull=True)


class PodcastDetailView(DetailView):
    queryset = PodcastIssue.objects.exclude(title__isnull=True)

from datetime import datetime, date, time
from optparse import make_option
import os

from django.core.management.base import BaseCommand
from django.conf import settings

from youtube_dl.extractor import YoutubeUserIE, YoutubePlaylistIE, YoutubeIE
from youtube_dl.utils import ExtractorError

from svv.models import PodcastIssue
from svv.utils import download_and_convert, get_downloader


class Command(BaseCommand):
    help = "Update videos list and, optionally, downloads new videos and converts them to MP3s"

    option_list = BaseCommand.option_list + (
        make_option('--only-info',
            action='store_true',
            dest='only_info',
            default=False,
            help='Don\'t download, only extract info (title, etc.), intended for initial db filling'),
        )

    def handle(self, *args, **options):
        downloader = get_downloader()
        ie_list = YoutubeUserIE(downloader=downloader)
        if not ie_list.suitable(settings.YOUTUBE_URL):
            ie_list = YoutubePlaylistIE(downloader=downloader)
        ie_video = YoutubeIE(downloader=downloader)
        result = ie_list.extract(settings.YOUTUBE_URL)[0]
        urls = [x["url"] for x in result["entries"]]
        if not options["only_info"]:
            for i, url in enumerate(urls):
                if PodcastIssue.objects.filter(youtube_url=url).exclude(file__isnull=True).\
                    exclude(file__exact="").exists():
                        urls = urls[:i]
                        break
        for url in reversed(urls):
            issue = None
            if PodcastIssue.objects.filter(youtube_url=url).exists():
                try:
                    issue = PodcastIssue.objects.get(youtube_url=url)
                except PodcastIssue.MultipleObjectsReturned:
                    # sanitize
                    PodcastIssue.objects.filter(youtube_url=url).delete()
                    issue = None

            if issue and issue.file:
                continue
            if issue and issue.title:
                continue

            try:
                info = ie_video.extract(url)[0]
            except ExtractorError:
                continue

            d = info["upload_date"]
            d = date(int(d[:4]), int(d[4:6]), int(d[6:8]))
            d = datetime.combine(d, time())

            desc = info["description"]
            short_desc = desc.split("\n")[0]

            if options["only_info"]:
                if issue:
                    issue.title=info["title"]
                    issue.description = desc
                    issue.short_description = short_desc
                    issue.pub_date = d
                    issue.save()
                else:
                    PodcastIssue.objects.create(
                        title=info["title"],
                        description=desc,
                        short_description=short_desc,
                        pub_date=d,
                        youtube_url=url,
                    )
                continue

            if issue:
                issue.title = info["title"]
                issue.description = desc
                issue.short_description = short_desc
                issue.pub_date = d
                issue.save()
            else:
                issue = PodcastIssue.objects.create(
                    title=info["title"],
                    description=desc,
                    short_description=short_desc,
                    pub_date=d,
                    youtube_url=url,
                )

            download_and_convert(issue, downloader, info)

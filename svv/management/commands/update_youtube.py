from datetime import datetime, date, time
from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings

from svv.models import PodcastIssue
from svv.utils import download_and_convert, get_list, get_video_info, get_audio_length


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
        urls = get_list(settings.YOUTUBE_URL)
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
                if issue.length_audio:
                    continue
            if issue and issue.title:
                if issue.length_video:
                    continue

            info = get_video_info(url)
            if not info:
                continue

            d = info["upload_date"]
            d = date(int(d[:4]), int(d[4:6]), int(d[6:8]))
            d = datetime.combine(d, time())

            desc = info["description"]
            short_desc = desc.split("\n")[0]

            if issue:
                issue.title = info["title"]
                issue.description = desc
                issue.short_description = short_desc
                issue.pub_date = d
                issue.length_video = int(info["duration"])
                issue.save()
            else:
                issue = PodcastIssue.objects.create(
                    title=info["title"],
                    description=desc,
                    short_description=short_desc,
                    pub_date=d,
                    length_video=info["duration"],
                    youtube_url=url,
                )

            if issue.file:
                issue.length_audio = get_audio_length(issue.file.path)
                issue.save()

            if options["only_info"]:
                continue

            download_and_convert(issue)

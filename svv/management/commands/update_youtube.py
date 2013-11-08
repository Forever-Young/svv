from subprocess import call
from datetime import date
import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File

from youtube_dl.FileDownloader import FileDownloader
from youtube_dl.extractor import YoutubeUserIE, YoutubePlaylistIE, YoutubeIE
#from youtube_dl.extractor import

from svv.models import PodcastIssue


class _YDL:
    def to_screen(self, message, skip_eol=False):
        pass  # print(message)

    def report_error(self, message, tb=None):
        print(message)  # TODO: log

class Command(BaseCommand):
    def handle(self, **kwargs):
        downloader = FileDownloader(_YDL(), {"format": settings.YOUTUBE_FORMAT})
        if settings.YOUTUBE_TYPE == "user":
            ie_user = YoutubeUserIE(downloader=downloader)
        if settings.YOUTUBE_TYPE == "playlist":
            ie_user = YoutubePlaylistIE(downloader=downloader)
        ie_video = YoutubeIE(downloader=downloader)
        result = ie_user.extract(settings.YOUTUBE_URL)[0]
        urls = [x["url"] for x in result["entries"]]
        for url in urls:
            if PodcastIssue.objects.filter(youtube_url=url).exists():
                break
            info = ie_video.extract(url)[0]
            tmp_dir = os.path.join(settings.TMP_DIR)
            tmp_video_fn = os.path.join(tmp_dir, 'video.{0}'.format(settings.YOUTUBE_EXT))
            downloader._do_download(tmp_video_fn, info)
            result_fn = os.path.join(tmp_dir, "result.mp3")
            call([os.path.join(settings.BASE_DIR, "scripts", "extract-speedup-file.sh"),
                  tmp_video_fn, settings.YOUTUBE_EXT, settings.SPEEDUP, tmp_dir, result_fn])

            d = info["upload_date"]
            d = date(int(d[:4]), int(d[4:6]), int(d[6:8]))
            desc = info["description"]
            short_desc = desc.split("\n")[0]
            issue = PodcastIssue.objects.create(
                title=info["title"],
                description=desc,
                short_description=short_desc,
                pub_date=d,
                youtube_url=url,
            )
            with open(result_fn, "rb") as f:
                issue.file.save("{0}.mp3".format(issue.youtube_id()), File(f))
                issue.save()
            os.remove(tmp_video_fn)
            os.remove(result_fn)

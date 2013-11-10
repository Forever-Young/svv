import os
from subprocess import call

from django.conf import settings
from django.core.files.base import File

from youtube_dl.FileDownloader import FileDownloader
from youtube_dl.extractor import YoutubeIE
from youtube_dl.utils import ExtractorError


class _YDL:
    def to_screen(self, message, skip_eol=False):
        pass  # print(message)

    def report_error(self, message, tb=None):
        print(message)  # TODO: log


def get_downloader():
    return FileDownloader(_YDL(), {"format": settings.YOUTUBE_FORMAT})


def download_and_convert(issue, downloader=None, info=None):
    if not downloader:
        downloader = get_downloader()
    if not info:
        ie = YoutubeIE(downloader=downloader)
        try:
            info = ie.extract(issue.youtube_url)[0]
        except ExtractorError:
            return False

    tmp_dir = os.path.join(settings.TMP_DIR)
    tmp_video_fn = os.path.join(tmp_dir, 'video.{0}'.format(settings.YOUTUBE_EXT))
    downloader._do_download(tmp_video_fn, info)
    result_fn = os.path.join(tmp_dir, "result.mp3")
    call([os.path.join(settings.BASE_DIR, "scripts", "extract-speedup-file.sh"),
          tmp_video_fn, settings.YOUTUBE_EXT, settings.SPEEDUP, tmp_dir, result_fn])

    with open(result_fn, "rb") as f:
        issue.file.save("{0}.mp3".format(issue.youtube_id()), File(f))
        issue.save()

    os.remove(tmp_video_fn)
    os.remove(result_fn)
    return True

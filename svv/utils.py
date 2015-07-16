import os
import unicodedata
from tempfile import mktemp

from subprocess import call, check_output, CalledProcessError

from django.conf import settings
from django.core.files.base import File

from youtube_dl.downloader import HttpFD
from youtube_dl.extractor import YoutubeUserIE, YoutubePlaylistIE, YoutubeIE
from youtube_dl.utils import ExtractorError
from youtube_dl import YoutubeDL


class _YDL(YoutubeDL):
    def to_stderr(self, message):
        print(message)

    def to_console_title(self, message):
        pass

    def trouble(self, *args, **kargs):
        pass

    def report_warning(self, *args, **kargs):
        pass

    def to_screen(self, message, skip_eol=False):
        pass

    def report_error(self, message, tb=None):
        print(message)  # TODO: log


class _FileDownloader(HttpFD):
    urlopen = YoutubeDL.urlopen
    _setup_opener = YoutubeDL._setup_opener

    def __init__(self, *args, **kwargs):
        res = super().__init__(*args, **kwargs)
        self._setup_opener()
        return res


def get_downloader():
    return _FileDownloader(_YDL(), {})


def get_list(url):
    downloader = get_downloader()
    ie_list = YoutubeUserIE(downloader=downloader)
    if not ie_list.suitable(url):
        ie_list = YoutubePlaylistIE(downloader=downloader)
    try:
        result = ie_list.extract(url)
    except ExtractorError:
        return []
    if result["_type"] == "url":
        ie_list = YoutubePlaylistIE(downloader=downloader)
    try:
        result = ie_list.extract(result["url"])
    except ExtractorError:
        return []
    return ["http://www.youtube.com/watch?v={0}".format(x["url"]) for x in result["entries"]]


def get_video_info(url):
    downloader = get_downloader()
    ie = YoutubeIE(downloader=downloader)
    try:
        return ie.extract(url)
    except ExtractorError:
        return None


def get_audio_length(path):
    try:
        return int(check_output(["mediainfo", "--output=Audio;%Duration%", path])) // 1000
    except (CalledProcessError, ValueError):
        return 0


def download_and_convert(issue):
    downloader = get_downloader()
    ie = YoutubeIE(downloader=downloader)
    try:
        info = ie.extract(issue.youtube_url)
    except ExtractorError:
        return False

    tmp_dir = os.path.join(settings.TMP_DIR)
    tmp_video_fn = mktemp(suffix="." + settings.YOUTUBE_EXT, dir=tmp_dir)
    try:
        downloader.download(tmp_video_fn, [x for x in info["formats"] if x["format_id"] == settings.YOUTUBE_FORMAT][0])
    finally:
        try:
            os.remove(tmp_video_fn + ".part")
        except FileNotFoundError:
            pass
    result_fn = mktemp(suffix=".mp3", dir=tmp_dir)
    call([os.path.join(settings.BASE_DIR, "scripts", "extract-speedup-file.sh"),
          tmp_video_fn, settings.YOUTUBE_EXT, settings.SPEEDUP, tmp_dir, result_fn])

    with open(result_fn, "rb") as f:
        issue.file.save("{0}.mp3".format(issue.youtube_id), File(f))
        issue.length_audio = get_audio_length(issue.file.path)
        issue.save()

    os.remove(tmp_video_fn)
    os.remove(result_fn)
    return True


def sanitize(path):
    # very simplified function from https://github.com/ksze/sanitize/tree/0bc3c3a9bce450119157c193ffaf5baeafe9a85a
    path = unicodedata.normalize('NFC', path)
    illegal_characters = {'\00', '\01', '\02', '\03', '\04', '\05', '\06', '\07', '\10', '\11', '\12', '\13', '\14',
                          '\15', '\16', '\17', '\20', '\21', '\22', '\23', '\24', '\25', '\26', '\27', '\30', '\31',
                          '\32', '\33', '\34', '\35', '\36', '\37', '/', '\\', ':', '*', '?', '"', '<', '>', '|',}
    for character in illegal_characters:
        path = path.replace(character, '')
    return path.rstrip(". ")

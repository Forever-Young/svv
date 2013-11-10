from svv_project.celery import app
from .utils import download_and_convert
from .models import PodcastIssue


@app.task
def download_and_convert_task(issue_pk):
    issue = PodcastIssue.objects.get(pk=issue_pk)
    if download_and_convert(issue):
        issue.skip_feed = True
        issue.save()
        return True
    return False

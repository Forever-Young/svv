from optparse import make_option
from datetime import date, timedelta

from django.core.management.base import BaseCommand, CommandError

from ...models import PodcastIssue


class Command(BaseCommand):
    help = "Clean stale media files"

    option_list = BaseCommand.option_list + (
        make_option('--days',
            action='store',
            dest='days',
            default=None,
            help='Select issues, which last view was more than N days ago'),
        make_option('--views',
            action='store',
            dest='views',
            default=None,
            help='Select issues, which view count is less than N'),
        )

    def handle(self, *args, **options):
        if options["days"] and options["views"]:
            raise CommandError('Please select only one filter option')

        if not options["days"] and not options["views"]:
            raise CommandError('Please select one filter option')

        try:
            if options["days"]:
                d = date.today() - timedelta(days=int(options["days"]))
                q = PodcastIssue.objects.filter(last_view__lte=d)
            else:
                q = PodcastIssue.objects.filter(views__lt=int(options["views"]))
        except ValueError:
            raise CommandError('Please specify integer')

        if not q:
            print('No suitable issues is found')
            return

        print('Found {} issues, delete? (y/N)'.format(q.count()))
        choice = input().lower()
        if choice == 'y':
            for issue in q:
                issue.delete_file()

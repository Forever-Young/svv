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
        make_option('--not-in-rss',
            action='store_true',
            dest='not_in_rss',
            default=False,
            help='Select issues, which are not in the RSS feed'),
        make_option('--confirm',
            action='store_true',
            dest='confirm',
            default=False,
            help='Don\'t ask for confirmation'),
        )

    def handle(self, *args, **options):
        if options["days"] and options["views"] and options["not_in_rss"]:
            raise CommandError('Please select only one filter option')

        if not options["days"] and not options["views"] and not options["not_in_rss"]:
            raise CommandError('Please select one filter option')

        if options["not_in_rss"]:
            q = PodcastIssue.objects.exclude(title__isnull=True).exclude(title__exact="").exclude(skip_feed=False) \
                       .exclude(file__exact="").exclude(file__isnull=True)[20:]
        else:
            q = PodcastIssue.objects.filter(skip_feed__exact=True).exclude(file='')
            try:
                if options["days"]:
                    d = date.today() - timedelta(days=int(options["days"]))
                    q = q.filter(last_view__lte=d)
                else:
                    q = q.filter(views__lt=int(options["views"]))
            except ValueError:
                raise CommandError('Please specify integer')

        if not q:
            print('No suitable issues is found')
            return

        choice = None
        if not options['confirm']:
            print('Found {} issues, delete? (y/N)'.format(q.count()))
            choice = input().lower()
        if options['confirm'] or choice == 'y':
            for issue in q:
                issue.delete_file()

from django.core.management.base import BaseCommand
from transitfuture import jobs
from optparse import make_option


class Command(BaseCommand):
    help = 'Gets the jobs'
    option_list = BaseCommand.option_list + (
        make_option(
            '-a', '--latitude',
            dest='latitude',
            type='str'
        ),
        make_option(
            '-o', '--longitude',
            dest='longitude',
            type='str'
        ),
    )

    def handle(self, *args, **options):
        latitude = options['latitude']
        longitude = options['longitude']
        print "latitude =", latitude, "longitude =", longitude
        total = jobs.get_jobs(latitude, longitude)
        print total

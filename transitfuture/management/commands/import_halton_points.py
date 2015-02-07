from django.core.management.base import NoArgsCommand
from transitfuture.models import HaltonPoint, BlockBoundary, CensusBlock
from transitfuture.halton import halton_points, job_coordinates


class Command(NoArgsCommand):
    help = 'Computes and stores halton point data'

    def handle(self, *args, **options):
        jobs_filename = 'jobs.json'
        for data in job_coordinates(jobs_filename):
            queryset = CensusBlock.objects.filter(census_block=data['geoId'])
            print "checking block", data['geoId']
            if queryset.exists():
                census_block = queryset.first()
                print "found it", census_block
                for coord in data['coordinates']:
                    BlockBoundary.objects.create(
                        census_block=census_block,
                        latitude=str(coord[1])[:7],
                        longitude=str(coord[0])[:8]
                    )
                min_x = min(coord[0] for coord in data['coordinates'])
                min_y = min(coord[1] for coord in data['coordinates'])
                max_x = max(coord[0] for coord in data['coordinates'])
                max_y = max(coord[1] for coord in data['coordinates'])
                if data['attributes']:
                    for att, count in data['attributes'].iteritems():
                        halton_result = halton_points(
                            data['coordinates'],
                            count,
                            min_x,
                            min_y,
                            max_x - min_x,
                            max_y - min_y
                        )
                        for halton_point in halton_result:
                            HaltonPoint.objects.create(
                                census_block=census_block,
                                industry=str(att)[:25],
                                longitude=str(halton_point[0])[:8],
                                latitude=str(halton_point[1])[:7],
                            )
            else:
                print "didn't find it"

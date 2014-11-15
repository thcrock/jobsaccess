from django.core.management.base import BaseCommand
from urllib import urlopen
import gzip
from StringIO import StringIO
import csv
from transitfuture.models import CensusBlock

class Command(BaseCommand):
    help = 'Imports US Census LODES data'


    def handle(self, *args, **options):
        for segment in ('S000', 'SA01', 'SA02', 'SA03', 'SE01', 'SE02', 'SE03', 'SI01', 'SI02', 'SI03'):
            url = urlopen("http://lehd.ces.census.gov/data/lodes/LODES7/il/wac/il_wac_{}_JT00_2011.csv.gz".format(segment))
            s = StringIO(url.read())
            with gzip.GzipFile(fileobj=s) as f:
                reader = csv.reader(f)
                header_row = reader.next()
                header = {}
                for (i, field) in enumerate(header_row):
                    header[i] = field
                for row in reader:
                    atts = dict((header[i], value) for (i, value) in enumerate(row))
                    atts['workforce_segment'] = segment
                    atts['census_block'] = atts['w_geocode']
                    del atts['w_geocode']
                    del atts['createdate']
                    obj = CensusBlock(**atts)
                    obj.save()

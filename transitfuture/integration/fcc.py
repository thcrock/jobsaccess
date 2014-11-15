import json
import urllib
import urllib2

from transitfuture.models import BlockLocations, CensusBlock


def census_blocks(latitude, longitude):
    latitude = str(latitude)[:12]
    longitude = str(longitude)[:12]
    print "checking", latitude, longitude
    queryset = BlockLocations.objects.filter(
        latitude=latitude,
        longitude=longitude
    )
    if queryset.exists():
        print "it exists"
        return [row.census_block_id for row in queryset.all()]

    data = urllib.urlencode((
        ('format', 'json'),
        ('latitude', latitude),
        ('longitude', longitude),
        ('showall', True),
    ))
    url = "http://data.fcc.gov/api/block/find?{}".format(data)
    result = urllib2.urlopen(url)
    response = json.loads(result.read())['Block']
    if 'intersection' in response:
        blocks = [node['FIPS'] for node in response['intersection']]
    else:
        blocks = [response['FIPS']]
    print "BLOCKS =", blocks
    for block in blocks:
        print "seeing if", block, "exists"
        queryset = CensusBlock.objects.filter(census_block=block)
        if queryset.exists():
            print "creating block"
            BlockLocations.objects.create(
                latitude=latitude,
                longitude=longitude,
                census_block=queryset.first(),
            )
        else:
            print "why doesn't it exist?"

    return blocks

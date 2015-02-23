import json
import urllib
import urllib2

from transitfuture.models import BlockLocations, CensusBlock


def census_blocks(latitude, longitude):
    latitude = str(latitude)[:7]
    longitude = str(longitude)[:8]
    queryset = BlockLocations.objects.filter(
        latitude=latitude,
        longitude=longitude
    )
    if queryset.exists():
        #print "Already found this one"
        return [row.census_block.census_block for row in queryset.all()]

    data = urllib.urlencode((
        ('format', 'json'),
        ('latitude', latitude),
        ('longitude', longitude),
        ('showall', True),
    ))
    url = "http://data.fcc.gov/api/block/find?{}".format(data)
    #print "Querying url", url
    result = urllib2.urlopen(url)
    response = json.loads(result.read())['Block']
    if 'intersection' in response:
        blocks = [node['FIPS'] for node in response['intersection']]
    else:
        blocks = [response['FIPS']]
    for block in blocks:
        queryset = CensusBlock.objects.filter(census_block=block)
        if queryset.exists():
            BlockLocations.objects.create(
                latitude=latitude,
                longitude=longitude,
                census_block=queryset.first(),
            )
        else:
            census_block = CensusBlock.objects.create(
                census_block=block
            )
            BlockLocations.objects.create(
                latitude=latitude,
                longitude=longitude,
                census_block=census_block,
            )

    return blocks

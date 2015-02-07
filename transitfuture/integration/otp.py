import json
import urllib
import urllib2
from transitfuture import models


def reachable_coordinates(
    latitude,
    longitude,
    depart_time,
    transit_time,
    phase_id,
    lookup_key
):
    coordinates = models.ReachableCoordinates.objects.filter(
        latitude_start=latitude,
        longitude_start=longitude,
        depart_time=depart_time,
        transit_time=transit_time,
        phase_achieved_id=phase_id
    )

    if coordinates.exists():
        otp_coords = [
            (result.longitude_reachable, result.latitude_reachable)
            for result in coordinates
        ]
    else:
        otp_url = models.PhaseAchieved.objects.get(pk=phase_id).url
        data = urllib.urlencode((
            ('layers', 'traveltime'),
            ('styles', 'mask'),
            ('fromPlace', "{},{}".format(latitude, longitude)),
            ('toPlace', '41.9430420, -87.6416480'),  # doesn't matter
            ('mode', 'TRANSIT,WALK'),
            ('time', depart_time),
            ('maxWalkDistance', 10000),
            ('walkSpeed', 1.38),
            ('walkTime', transit_time),
            ('output', 'POINTS'),
            ('batch', True)
        ))
        url = '{}/opentripplanner-api-webapp/ws/iso?{}'.format(otp_url, data)
        print "Querying ", url
        req = urllib2.Request(url)
        otp_coords = json.loads(urllib2.urlopen(req).read())['coordinates']

        print "Bulk creating"
        models.ReachableCoordinates.objects.bulk_create((
            models.ReachableCoordinates(
                latitude_start=latitude,
                longitude_start=longitude,
                depart_time=depart_time,
                transit_time=transit_time,
                phase_achieved_id=phase_id,
                longitude_reachable=str(coordinate[0])[:8],
                latitude_reachable=str(coordinate[1])[:7],
                lookup_key=str(lookup_key),
            )
        ) for coordinate in otp_coords)
        print "Bulk create done"

    return otp_coords

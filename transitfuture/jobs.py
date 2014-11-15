from transitfuture.integration import otp, fcc
from transitfuture.models import CensusBlock


def get_jobs(
    latitude,
    longitude,
    depart='2014-06-06T09:00:00',
    transit_time=10
):
    reachable_coordinates = otp.reachable_coordinates(
        latitude,
        longitude,
        depart,
        transit_time,
        1
    )
    num_coordinates = len(reachable_coordinates)
    print num_coordinates, "reachable coordinates"
    total_blocks = {}
    for i, (lon, lat) in enumerate(reachable_coordinates):
        if i % 50 == 0:
            print i, "out of", num_coordinates
        blocks = fcc.census_blocks(lat, lon)
        print "returned blocks = ", blocks
        for block in blocks:
            if block not in total_blocks:
                print "Looking for", block
                census_blocks = CensusBlock.objects.filter(
                    census_block=block,
                    workforce_segment='S000',  # all segments
                ).all()
                if len(census_blocks) > 1:
                    raise ValueError('too many blocks')
                for row in census_blocks:
                    total_blocks[block] = row
    return sum(
        total_blocks[block].C000  # all jobs
        for block in total_blocks
    )

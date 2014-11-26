from django.core.cache import cache

from transitfuture.integration import otp, fcc
from transitfuture.models import CensusBlock
import time


def get_jobs(
    latitude,
    longitude,
    depart=None,
    transit_time=None
):
    depart = depart or '2014-06-06T09:00:00'
    transit_time = transit_time or 10
    reachable_coordinates = otp.reachable_coordinates(
        latitude,
        longitude,
        depart,
        transit_time,
        1
    )
    total_blocks = {}
    for i, (lon, lat) in enumerate(reachable_coordinates):
        cache_key = 'block|{}|{}'.format(lat, lon)
        blocks = cache.get(cache_key)
        if not blocks:
            blocks = fcc.census_blocks(lat, lon)
            cache.set(cache_key, blocks)
        else:
            print "Cache hit baby"

        for block in blocks:
            if block not in total_blocks:
                cache_key = 'census_data|{}'.format(block)
                census_blocks = cache.get(cache_key)
                if not census_blocks:
                    census_blocks = CensusBlock.objects.filter(
                        census_block=block,
                        workforce_segment='S000',  # all segments
                    ).all()
                    cache.set(cache_key, census_blocks)

                if len(census_blocks) > 1:
                    raise ValueError('too many blocks')
                for row in census_blocks:
                    total_blocks[block] = row
    return total_blocks

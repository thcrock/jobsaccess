from django.core.management.base import NoArgsCommand
from django.db import connection
import requests
from transitfuture.integration import otp


class Command(NoArgsCommand):

  def blocks_from_coords(self, coords):
    return set(block for lon, lat in coords for block in self.blocks_from_coord(lon, lat))

  def blocks_from_coord(self, lon, lat):
    with connection.cursor() as c:
      query = """
        select
          distinct(geoid10)
          from blocks
          where (ST_contains(
            geom,
            st_transform(ST_Point(cast({longitude} as float), cast({latitude} as float))::geography::geometry, 4269)
          ))
      """.format(latitude=lat, longitude=lon)
      c.execute(query)
      results = c.fetchall()
      for row in results:
        yield row[0]

  def handle(self, *args, **options):
    with connection.cursor() as c:
      query = "select geoid10, st_astext(st_centroid(geom)) from blocks limit 100"
      c.execute(query)
      results = c.fetchall()
    for r in results:
      lon, lat = r[1][6:-1].split(' ')
      depart = '2015-02-06T09:00:00'
      transit_time = 30
      try:
        coords = otp.transitshed(
            lat,
            lon,
            depart,
            transit_time,
            1,
        )
        blocks = self.blocks_from_coords(coords)
        print blocks
      except StandardError, e:
        print e
        pass

from django import http
from django.conf import settings
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.core.serializers.json import DjangoJSONEncoder
from collections import Counter, defaultdict
import json
from PIL import Image, ImageDraw
import uuid

from transitfuture.forms import JobsForm, BikingForm
from transitfuture.integration import fcc, otp
from transitfuture.jobs import get_jobs
from transitfuture.models import BlockLocations
from transitfuture.slippytile import tile_offset, lon2tilex, lat2tiley, tile2linestring

INDUSTRIES = {
    'information': '46DFD3',
    'transport_utilities': "FFFF33",
    "trade": "E41A1C",
    "construction_manufacturing": "A65628",
    "public_admin": "FF7F00",
    "leisure_hospitality": "FB9A99",
    "finance": "00AA0E",
    "health": "286FAA",
    "education": "6A3D9A",
    "professional": "A6CEE3",
}


class JsonHttpResponse(http.HttpResponse):
    """HttpResponse which JSON-encodes its content and whose Content-Type defaults
    to "application/json".

    """
    def __init__(
        self,
        content=None,
        content_type='application/json',
        *args,
        **kws
    ):
        super(JsonHttpResponse, self).__init__(
            content=json.dumps(content, cls=DjangoJSONEncoder),
            content_type=content_type, *args, **kws
        )


@require_GET
def allblocks(request):
    return JsonHttpResponse(
        list(BlockLocations.objects.
             distinct('census_block_id').
             values('latitude', 'longitude')
             )
    )


@require_GET
def blockspage(request):
    return render(request, 'blocks.html')


@require_GET
def otpresults(request):
    form = JobsForm(request.GET)
    if not form.is_valid():
        return JsonHttpResponse(form.errors, status=400)

    lookup_key = str(uuid.uuid4())
    data = form.cleaned_data
    depart = data['depart'] or '2015-02-06T09:00:00'
    transit_time = data['transit_time'] or 5
    lat = data['latitude'][:7]
    lon = data['longitude'][:8]
    otp.reachable_coordinates(
        lat,
        lon,
        depart,
        transit_time,
        1,
        lookup_key
    )

    results = None
    cols = [
        'C000',
    ]
    select_clause = ",\n".join("max(\"{val}\")".format(val=val) for val in cols)
    with connection.cursor() as c:
        full_query = """
            select
                census_block,
                max(latitude_reachable),
                max(longitude_reachable),
                {}
            from reachable_coordinates
            left join blocks on (ST_contains(geom, ST_Point(cast(longitude_reachable as float), cast(latitude_reachable as float))::geography::geometry))
            left join census_blocks on (geoid10 = census_block and workforce_segment = 'S000')
            where lookup_key = '{}'
            group by census_block
        """.format(select_clause, lookup_key)
        print full_query
        c.execute(full_query)
        results = c.fetchall()

    return JsonHttpResponse({'lookup_key': lookup_key, 'data': results})


@require_GET
def otpresultspage(request):
    print settings.DOMAIN
    print settings.PORT
    return render(request, 'otpresults.html', {
        'domain': settings.DOMAIN,
        'port': settings.PORT,
    })


@require_GET
def tile(request, z, x, y, lookup_key):
    """
        Given a list of census blocks (with sample lat/lon and jobs data), for each census block:
        1. Lookup boundary for each census block
        2. Transform each boundary coordinate into tile offset, and crop
        3. Draw the polygon boundary
        4. For each industry, lookup halton points, scale, transform, crop, and draw
    """
    img = Image.new("RGBA", (256,256), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    linestring = 'linestring({})'.format(tile2linestring(x, y, z))
    print x, y, linestring
    with connection.cursor() as curs:
        boundary_sql = """
            select
                geoid10,
                st_asgeojson(geom)
            from
                blocks
                join reachable_coordinates on (ST_contains(geom, ST_Point(cast(longitude_reachable as float), cast(latitude_reachable as float))::geography::geometry))
                left join census_blocks on (geoid10 = census_blocks.census_block)
            where
                st_intersects(st_polygon(st_geomfromtext('{}'), 4326), geom) and
                lookup_key = '{}'
        """.format(linestring, lookup_key)
        curs.execute(boundary_sql)
        untransformed_boundary = curs.fetchall()
    boundary_lookup = defaultdict(list)
    for census_block, geometry in untransformed_boundary:
        data = json.loads(geometry)
        boundary_lookup[census_block] = data['coordinates'][0]
    zoom = int(z)
    y = int(y)
    x = int(x)
    for block_id, polygon in boundary_lookup.iteritems():
        for coord_list in polygon:
            real_boundary_coords = [
                tile_offset(lat, lon, x, y, zoom)
                for lon, lat in coord_list
            ]
            #draw.polygon(real_boundary_coords, outline=(50, 50, 50), fill=(125,125,125))
    with connection.cursor() as curs:
        halton_sql = """
            select
                census_block,
                industry,
                hp.latitude,
                hp.longitude
            from
                blocks
                join reachable_coordinates on (ST_contains(geom, ST_Point(cast(longitude_reachable as float), cast(latitude_reachable as float))::geography::geometry))
                join halton hp on (geoid10 = hp.census_block)
            where
                st_intersects(st_polygon(st_geomfromtext('{}'), 4326), geom) and
                lookup_key = '{}'
        """.format(linestring, lookup_key)
        curs.execute(halton_sql)
        coords = curs.fetchall()
    if coords:
        scaled_coords = [
            tile_offset(lat, lon, x, y, zoom)
            for block, ind, lat, lon in coords
        ]
        if scaled_coords:
            print "found a job", scaled_coords
        draw.point(scaled_coords, fill=(255,0,0))
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response



@require_GET
def jobs(request):
    form = JobsForm(request.GET)
    if not form.is_valid():
        return JsonHttpResponse(form.errors, status=400)

    data = form.cleaned_data
    jobs = get_jobs(data['latitude'], data['longitude'], data['depart'], data['transit_time'])

    sums = Counter()
    attributes = (
        'C000',
        'CA01',
        'CA02',
        'CA03',
        'CE01',
        'CE02',
        'CE03',
        'CNS01',
        'CNS02',
        'CNS03',
        'CNS04',
        'CNS05',
        'CNS06',
        'CNS07',
        'CNS08',
        'CNS09',
        'CNS10',
        'CNS11',
        'CNS12',
        'CNS13',
        'CNS14',
        'CNS15',
        'CNS16',
        'CNS17',
        'CNS18',
        'CNS19',
        'CNS20',
        'CR01',
        'CR02',
        'CR03',
        'CR04',
        'CR05',
        'CR07',
        'CT01',
        'CT02',
        'CD01',
        'CD02',
        'CD03',
        'CD04',
        'CS01',
        'CS02',
        'CFA01',
        'CFA02',
        'CFA03',
        'CFA04',
        'CFA05',
        'CFS01',
        'CFS02',
        'CFS03',
        'CFS04',
        'CFS05',
    )
    for block in jobs:
        for attribute in attributes:
            sums[attribute] += getattr(jobs[block], attribute)
    return JsonHttpResponse(sums)


@require_GET
def bikeshedspage(request):
    return render(request, 'biking.html', {
        'domain': settings.DOMAIN,
        'port': settings.PORT,
    })


def bikeshed(request):
    form = BikingForm(request.GET)
    if not form.is_valid():
        return JsonHttpResponse(form.errors, status=400)

    data = form.cleaned_data

    reachable_polygon = otp.bikeshed(
        data['latitude'][:7],
        data['longitude'][:8],
        data['bike_speed'],
        data['safety'],
        data['slope'],
        data['quick'],
        data['transit_time'],
    )
    return JsonHttpResponse({
        'type': 'Feature',
        'geometry': reachable_polygon,
    })

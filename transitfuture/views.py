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

from transitfuture.forms import JobsForm
from transitfuture.integration import fcc, otp
from transitfuture.jobs import get_jobs
from transitfuture.models import BlockLocations
from transitfuture.slippytile import tile_offset, lon2tilex, lat2tiley

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
    depart = data['depart'] or '2014-10-06T09:00:00'
    transit_time = data['transit_time'] or 5
    lat = data['latitude'][:7]
    lon = data['longitude'][:8]
    reachable_coordinates = otp.reachable_coordinates(
        lat,
        lon,
        depart,
        transit_time,
        1,
        lookup_key
    )

    temp_table_query = """
        with coords as (
            select
                latitude_reachable as latitude,
                longitude_reachable as longitude
            from reachable_coordinates
            where
                latitude_start = '{lat}' and
                longitude_start = '{lon}' and
                depart_time = '{depart}' and
                transit_time = {transit_time}
        )
    """.format(lat=lat, lon=lon, depart=depart, transit_time=transit_time)
    missing_coordinates = None
    with connection.cursor() as c:
        missing_query = """
            {}
            select latitude, longitude
            from coords
            left join block_locations using (latitude, longitude)
            where block_locations.id is null
            group by 1, 2
        """.format(temp_table_query)
        c.execute(missing_query)
        missing_coordinates = c.fetchall()
    print len(reachable_coordinates),\
        "reachable coordinates,",\
        len(missing_coordinates),\
        "missing coordinates"
    for i, (reachable_lat, reachable_lon) in enumerate(missing_coordinates):
        fcc.census_blocks(reachable_lat, reachable_lon)
        if i % 10 == 0:
            print i, "of", len(missing_coordinates), "coordinates searched"

    results = None
    cols = [
        'census_block',
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
    ]
    select_clause = ",\n".join("max(\"{val}\")".format(val=val) for val in cols)
    with connection.cursor() as c:
        full_query = """
            {}
            select
                census_block,
                max(latitude),
                max(longitude),
                {}
            from coords
            join block_locations using (latitude, longitude)
            join census_blocks on (
                block_locations.census_block_id = census_blocks.id and
                census_blocks.workforce_segment = 'S000'
            )
            group by census_block
        """.format(temp_table_query, select_clause)
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
    with connection.cursor() as curs:
        boundary_sql = """
            select
                census_block,
                bb.latitude,
                bb.longitude
            from
                reachable_coordinates rc
                join block_locations bl on (bl.latitude = rc.latitude_reachable and bl.longitude = rc.longitude_reachable)
                join census_blocks cb on (bl.census_block_id = cb.id and cb.workforce_segment = 'S000')
                join block_boundaries bb on (bb.census_block_id = cb.id)
            where lookup_key = '{}'
        """.format(lookup_key)
        curs.execute(boundary_sql)
        untransformed_boundary = curs.fetchall()
    boundary_lookup = defaultdict(list)
    for census_block, lat, lon in untransformed_boundary:
        boundary_lookup[census_block].append((lat,lon))

    zoom = int(z)
    y = int(y)
    x = int(x)
    for coord_list in boundary_lookup.values():
        real_boundary_coords = [
            tile_offset(lat, lon, zoom)
            for lat, lon in coord_list
            if lon2tilex(lon, zoom) == x and lat2tiley(lat, zoom) == y
        ]
        if len(real_boundary_coords) > 0:
            draw.polygon(real_boundary_coords, outline=(100, 100, 100), fill=(200,200,200))
    with connection.cursor() as curs:
        halton_sql = """
            select
                census_block,
                industry,
                hp.latitude,
                hp.longitude
            from
                reachable_coordinates rc
                join block_locations bl on (bl.latitude = rc.latitude_reachable and bl.longitude = rc.longitude_reachable)
                join census_blocks cb on (bl.census_block_id = cb.id and cb.workforce_segment = 'S000')
                join halton_points hp on (hp.census_block_id = cb.id)
            where lookup_key = '{}'
""".format(lookup_key)
        curs.execute(halton_sql)
        coords = curs.fetchall()
    if coords:
        scaled_coords = [
            tile_offset(lat, lon, zoom)
            for block, ind, lat, lon in coords
            if lon2tilex(lon, zoom) == x and lat2tiley(lat, zoom) == y
        ]
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

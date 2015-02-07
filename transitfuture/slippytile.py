import math

TILE_SIZE = 256
pixel_origin_y = TILE_SIZE / 2
pixel_origin_x = TILE_SIZE / 2
pixels_per_lon_degree = TILE_SIZE / 360;
pixels_per_lon_radian = TILE_SIZE / (2 * math.pi)


def latlontopoint(lat, lon):
    x = pixel_origin_x + lon * pixels_per_lon_degree
    siny = math.sin(math.radians(lat))
    y = pixel_origin_x + 0.5 * math.log((1 + siny) / (1 - siny)) * -pixels_per_lon_radian
    return (x, y)


def tile_number(lat, lon, zoom):
    return("" + str(zoom) + "/" + str(lon2tilex(lon, zoom)) + "/" + str(lat2tiley(lat, zoom)))


def lat2tiley(lat, zoom):
    return int(math.floor(
        lat2worldy(float(lat)) * num_tiles(zoom)
    ))

def lat2tileoffset(lat, zoom):
    world = lat2worldy(lat) * TILE_SIZE
    pixel = world * num_tiles(zoom)
    tile_start = lat2tiley(lat, zoom) * TILE_SIZE
    return pixel - tile_start

def lon2tileoffset(lon, zoom):
    world = lon2worldx(lon) * TILE_SIZE
    pixel = world * num_tiles(zoom)
    tile_start = lon2tilex(lon, zoom) * TILE_SIZE
    return pixel - tile_start


def lon2tilex(lon, zoom):
    return int(math.floor(
        lon2worldx(float(lon)) * num_tiles(zoom)
    ))

def num_tiles(zoom):
    return (1 << zoom)

def lat2worldy(lat):
    return (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2

def lon2worldx(lon):
    return (lon + 180) / 360

def tile_offset(lat, lon, zoom):
    return (
        lat2tileoffset(float(lat), zoom),
        lon2tileoffset(float(lon), zoom)
    )


def tile2lon(x, z):
    return x / math.pow(2.0, z) * 360.0 - 180


def tile2lat(y, z):
    n = math.pi - (2.0 * math.pi * y) / math.pow(2.0, z)
    return math.degrees(math.atan(math.sinh(n)))

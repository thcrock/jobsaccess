import math


def tile_number(lat, lon, zoom):
    xtile = int(math.floor(
        (lon + 180) / 360 * (1 << zoom)
    ))
    ytile = int(math.floor(
        (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * (1 << zoom)
    ))
    return("" + str(zoom) + "/" + str(xtile) + "/" + str(ytile))


def tile2lon(x, z):
    return x / math.pow(2.0, z) * 360.0 - 180


def tile2lat(y, z):
    n = math.pi - (2.0 * math.pi * y) / math.pow(2.0, z)
    return math.degrees(math.atan(math.sinh(n)))

import math


def tile_number(lat, lon, zoom):
    xtile = int(math.floor(
        (lon + 180) / 360 * (1 << zoom)
    ))
    ytile = int(math.floor(
        (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * (1 << zoom)
    ))
    return("" + str(zoom) + "/" + str(xtile) + "/" + str(ytile))


def tile_offset(lat, lon, zoom, x, y):
    print lat, lon, zoom, x, y
    min_lat = tile2lat(y+1, zoom)
    max_lat = tile2lat(y, zoom)
    min_lon = tile2lon(x, zoom)
    max_lon = tile2lon(x+1, zoom)

    lat_offset = lat - min_lat
    lon_offset = lon - min_lon
    scaled_lat_offset = lat_offset*256 / (max_lat - min_lat)
    scaled_lon_offset = lon_offset*256 / (max_lon - min_lon)
    return (scaled_lat_offset, scaled_lon_offset)


def tile2lon(x, z):
    return x / math.pow(2.0, z) * 360.0 - 180


def tile2lat(y, z):
    n = math.pi - (2.0 * math.pi * y) / math.pow(2.0, z)
    return math.degrees(math.atan(math.sinh(n)))

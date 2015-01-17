import json
import math
import random
import sys

def job_coordinates(jobs_filename):
    with open(jobs_filename, 'r') as jobs_file:
        jobs = json.load(jobs_file)
    for job in jobs['features']:
        yield {
            'coordinates': job['geometry']['coordinates'][0][0],
            'attributes': job['attributes'],
            'geoId': job['geoId']
        }


def run(jobs_filename):
    for data in job_coordinates(jobs_filename):
        min_x = min(coord[0] for coord in data['coordinates'])
        min_y = min(coord[1] for coord in data['coordinates'])
        max_x = max(coord[0] for coord in data['coordinates'])
        max_y = max(coord[1] for coord in data['coordinates'])
        coords = halton_points(
            data['coordinates'],
            sum(data['attributes'].values()),
            min_x,
            min_y,
            max_x - min_x,
            max_y - min_y
        )
        print coords


def contains(boundary_points, x, y):
    i = 0
    j = 0
    result = False
    while i < len(boundary_points):
        if (
            (boundary_points[i][1] > y) is not (boundary_points[j][1] > y) and
            (x < (boundary_points[j][0] - boundary_points[i][0]) * (y - boundary_points[i][1]) / (boundary_points[j][1]-boundary_points[i][1]) + boundary_points[i][0])
        ):
            result = not result
        i += 1
        j = i
    return result;


def halton_number(index, base):
    base = float(base)
    result = 0
    fraction = 1.0 / base
    i = index
    while i > 0:
        result = result + fraction * (i % base)
        i = (int)(math.floor(i / base))
        fraction = fraction / base
    return result


def halton_points(coordinates, num_points, min_x, min_y, width, height):
    coord_len = num_points
    coords = []

    if num_points > 0:
        basei = 2
        basej = 3

        baseX = min_x
        baseY = min_y

        i = 0
        j = random.randint(0, sys.maxint)

        if(j + coord_len > sys.maxint):
            j = j - coord_len

        while i < coord_len:
            x = baseX + width * halton_number(j + 1, basei)
            y = baseY + height * halton_number(j + 1, basej)

            j += 1

            if not contains(coordinates, x, y):
                next

            coords.append([x, y])
            i += 2
    return coords

if __name__ == '__main__':
    run('jobs.json')

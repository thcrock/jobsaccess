from django.core.management.base import BaseCommand
import requests
import csv

class Command(BaseCommand):
    help = 'Download ridership by route and use to split bus stop boarding data into routes'


    def handle(self, *args, **options):
        route_totals_url = 'https://data.cityofchicago.org/resource/jyb9-n7fm.json'
        route_totals = requests.get(
            route_totals_url,
            params={ 'date': '2012-10-01T00:00:00', 'daytype': 'W' }
        ).json()
        lookup = dict((route['route'], int(route['rides'])) for route in route_totals)
        print "Populated Lookup Table"

        boardings_url = 'https://data.cityofchicago.org/resource/mq3i-nnqe.json'
        boardings = requests.get(
            boardings_url,
            params={ 'daytype': 'Weekday' },
        ).json()
        with open('cta_boardings.csv', 'w') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(['stop_id', 'on_street', 'cross_street', 'route', 'boardings', 'location'])
            for stop in boardings:
                routes = [route.strip(' ') for route in stop['routes'].split(',')]
                missing_routes = [route for route in routes if route not in lookup]
                total_boardings_for_routes = sum(lookup[route] for route in routes if route in lookup)
                average = total_boardings_for_routes / (len(routes) - len(missing_routes))
                total_boardings_for_routes += average*len(missing_routes)
                route_weights = dict((route, float(lookup.get(route, average)) / total_boardings_for_routes) for route in routes)
                for route in routes:
                    normalized_boardings = round(float(stop['boardings']) * route_weights[route], 1)
                    writer.writerow([stop['stop_id'], stop['on_street'], stop['cross_street'], route, normalized_boardings, stop['location']])

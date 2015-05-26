from django.apps import AppConfig
from shapely.geometry import shape
from fiona import collection
from rtree import index
import csv

class TransitFutureConfig(AppConfig):
    name = 'transitfuture'
    verbose_name = "Transit Future"
    def ready(self):
        #self.load_shapes()
        self.load_jobs()

    def load_shapes(self):
        # load polygons and spatial index
        print "In app config"
        if not hasattr(self, 'polygons'):
            print "loading polygons"
            filename = 'data/tl_2014_17_tabblock10.shp'
            with collection(filename, "r") as input:
                self.polygons = []
                self.block_lookup = {}
                for polygon in input:
                    self.block_lookup[len(self.polygons)] = polygon['properties']['GEOID10']
                    self.polygons.append(shape(polygon['geometry']))
            print "Done loading polygons", len(self.polygons)
        else:
            print "short-circuited through polygon creation"

        if not hasattr(self, 'spatial_index'):
            self.spatial_index = index.Index()
            count = -1
            for shp in self.polygons:
                count += 1
                self.spatial_index.insert(count, shp.bounds)
            print "Done creating spatial index"
        else:
            print "short-circuited through spatial index creation"


    def load_jobs(self):
        # load jobs by census block
        if not hasattr(self, 'jobs_lookup'):
            self.jobs_lookup = {}
            with open('data/il_wac_S000_JT00_2011.csv') as jobs_file:
                jobs_iter = csv.reader(jobs_file)
                jobs_iter.next()
                for row in jobs_iter:
                    self.jobs_lookup[row[0]] = row[1]

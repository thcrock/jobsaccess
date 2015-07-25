from django.apps import AppConfig
from django.conf import settings
import cPickle as pickle

class TransitFutureConfig(AppConfig):
    name = 'transitfuture'
    verbose_name = "Transit Future"
    def ready(self):
      self.jobs = pickle.load(open(settings.JOBS_PATH, "rb"))
      print "done with jobs"
      self.shapes = pickle.load(open(settings.SHAPES_PATH, "rb"))
      print "done with shapes"
      self.blocks = pickle.load(open(settings.BLOCKS_PATH, "rb"))
      print "done with blocks"
      self.spatial_index = pickle.load(open(settings.SPATIALINDEX_PATH, "rb"))
      print "done with index"

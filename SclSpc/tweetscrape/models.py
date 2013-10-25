from django.db import models
from django.db import transaction, IntegrityError
from dataman.models import Location, Tag, CheckIn
from django.contrib.gis.geos import Point
from datetime import datetime
from twython import Twython

#Twitter Interface
#Twitter API info
class TwitterInterface(models.Model):
  key = models.CharField(max_length=150, null = False)
  secret = models.CharField(max_length=150, null = False)
  token = models.CharField(max_length=150)
  
  def __unicode__(self):
    return u'Twitter Auth'
    
  def _grab_token(self):
    self.access_token = t.obtain_access_token()
    return

  def _twitter_interface(self):
    if self.token == "":
      self._grab_token()
    else:
      t = Twython(self.key, self.token)
    return t
    
  def test_geo(self):
    lat = 34.050238
    lon = -118.244828
    rad = 32
    
    twit = self._twitter_interface()
    


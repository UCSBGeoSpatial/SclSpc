from django.db import models
from django.db import transaction, IntegrityError
from dataman.models import Location, Tag, CheckIn
from django.contrib.gis.geos import Point
from datetime import datetime
from twython import Twython, TwythonStreamer

#Twitter Interface
#Twitter API info
class _stream_interface(TwythonStreamer):
  def on_success(self, data):
    if "Foursquare" in data['source']:
      print data['text']
      print data['coordinates']['coordinates'][0]
      print data['coordinates']['coordinates'][1]
      print data['user']['screen_name']
      
  def on_error(self, status_code, data):
    print status_code
      
class TwitterInterface(models.Model):
  key = models.CharField(max_length=150, null = False)
  secret = models.CharField(max_length=150, null = False)
  token = models.CharField(max_length=150, blank = True)
  
  def __unicode__(self):
    return u'Twitter Auth'
    
  def _oauth2(self):
    t = Twython(self.key, self.secret, oauth_version=2)
    self.token = t.obtain_access_token()
    return self.token

  def _twitter_interface(self):
    self._oauth2()
    t = Twython(self.key, access_token=self.token)
    return t
    
  def overview_scrape(self):
    sw_lat = "33.564041"
    sw_lon = "-118.871573"
    ne_lat = "34.337914"
    ne_lon = "-117.486441"
    oauth_token = "365833866-c7WGKzDlcFMAcZXOBIBpjXaXzDbMyw1hBo8XCRqa"
    oauth_secret = "BNvbni46FpZ18SEQhx1qneulAdb8IUCZgNoqMdX06c9Nr"
    twit = _stream_interface(self.key, self.secret, oauth_token, oauth_secret)
    twit.statuses.filter(locations=sw_lon + ',' + sw_lat + ',' + ne_lon + ',' + ne_lat)    
    
    
    

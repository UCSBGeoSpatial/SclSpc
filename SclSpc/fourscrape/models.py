from django.db import models
from dataman.models import Place, Category
import foursquare

class FoursquareInterface(models.Model):
  uid = models.CharField(max_length=150, null = False)
  secret = models.CharField(max_length=150, null = False)
  
  def __unicode__(self):
    return u'Foursquare Auth'
  
  def _foursquare_interface(self):
    fs = foursquare.Foursquare(client_id=self.uid, client_secret=self.secret)
    return fs
                
  def parse_cats(self, place, categories):
    for category in categories:
      try:
        c = Category.objects.filter(fs_id = category['id'])[0]
      except:
        c = Category(name = category['name'], pluralName = category['pluralName'], shortName = category['shortName'], fs_id = category['id'])
        c.save()
      place.foursq_categories.add(c)
      if category['primary']:
        place.foursq_primary_cat = c
    place.save()
    
  def place_scrape(self):
    places_without_fs = Place.objects.filter(foursq_id=None).exclude(name='')
    fs = self._foursquare_interface()
    
    for place in places_without_fs:
      lat = str(place.location.lat)
      lon = str(place.location.lon)
      name = place.name.encode('ascii', 'ignore')
      try:
        seed = fs.venues.search(params={'ll': lat+ ',' + lon , 'query':name})['venues'][0]
        if seed['location']['distance'] == 0:
          place.foursq_id = seed['id']
          try:
            place.twitter_handle = seed['contact']['twitter']
          except:
            continue
          try:
            self.parse_cats(place, seed['categories'])
          except:
            continue
      except:
        continue
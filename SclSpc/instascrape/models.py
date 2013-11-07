from django.db import models
from django.db import transaction, IntegrityError
from dataman.models import Location, Tag, Pic, Place
from django.contrib.gis.geos import Point
from datetime import datetime
from random import randrange
import instagram

#Instagram Interface
#Instagram API info
class InstagramInterface(models.Model):
  uid = models.CharField(max_length=150, null = False)
  secret = models.CharField(max_length=150, null = False)
  
  
  def __unicode__(self):
    return u'Instagram Auth'
    
  def _instagram_interface(self):
    i = instagram.InstagramAPI(client_id = self.uid, client_secret = self.secret)
    return i
    
  def overview_scrape(self):
    all_locations = Location.objects.all()
    seed = all_locations[randrange(len(all_locations))]
    inst = self._instagram_interface()
    photos = inst.media_search(5000, 1000, seed.lat, seed.lon)
    #self.save_pics(photos)
    return photos

  def spot_scrape(self):
    all_places = Place.objects.all()
    seed = all_places[randrange(len(all_places))]
    inst = self._instagram_interface()
    photos = inst.location_recent_media(100, None, seed.venueid)
    #self.save_pics(photos)
    return photos[0]
    
  def place_scrape(self):
    all_places = Place.objects.all()
    seed = all_places[randrange(len(all_places))]
    
    while seed.name:
      seed = all_places[randrange(len(all_places))]
      
    inst = self._instagram_interface()
    if seed.venueid != '0':
      place = inst.location(seed.venueid)
      seed.name = place.name
      seed.save()
    
    return
    
  def save_pics(self, thelist):
    for photo in thelist:
        image = photo.images['standard_resolution'].url
        try:
          caption = photo.caption.text      
        except:
          caption = "nocap"    
        c_at = photo.created_time
        
        #Location check
        location = self.parse_location(photo.location)
        
        #Create new pic
        p = self.parse_pic(caption, location, image, c_at)
        
        #Tag attribution
        try:
          tags = photo.tags
          self.parse_tags(p, tags)
        except:
          continue
    return
  
  def parse_pic(self, title, l, url_l, c_at):
    try:
      p = Pic.objects.filter(url = url_l)[0]
    except:
      p = Pic(name = title, location = l, url = url_l, created_at = c_at)
      try:
        p.save()
      except IntegrityError:
        transaction.rollback()
        print("An error has occured in saving the picture\n")
      
    return p
  
  def parse_location(self, location):
    latitude = location.point.latitude
    longitude = location.point.longitude
    venue = location.id
    
    try:
      l = Location.objects.filter(lon = longitude, lat = latitude)[0]
    except:
      pnt = Point(longitude, latitude)
      l = Location(lon = longitude, lat = latitude, point = pnt)
      l.save()
    
    if venue != None:  
      try:
        p = Place.objects.filter(venueid = venue)[0]
      except:
        p = Place(venueid=venue, location=l)
        p.save()
      
    return l
  
  def parse_tags(self, p, tags):
	 #Cycles thru picture tags
    for non_parsed in tags:
	   parsed = str(non_parsed)
	   tag = parsed.replace("Tag: ", "")
	   try:
	     t = Tag.objects.filter(content = tag)[0]
	   except:
	     t = Tag(content = tag)
	     t.save()
	              
	   p.tags.add(t)
	      
    return
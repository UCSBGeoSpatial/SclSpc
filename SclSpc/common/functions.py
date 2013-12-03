from dataman.models import Location, Pic, Place, Tag
from django.db import transaction, IntegrityError
from django.contrib.gis.geos import Point
#A cornucopia of functions.

##Parse Location, very common
def parse_location(location):
  latitude = location.point.latitude
  longitude = location.point.longitude
  venue = location.id
  
  try:
    l = Location.objects.filter(lon = longitude, lat = latitude)[0]
  except:
    pnt = Point(longitude, latitude)
    l = Location(lon = longitude, lat = latitude, point = pnt)
    try:
      l.save()
    except:
      transaction.rollback()
      print("An error has occured in saving the location\n")
    
  
  if venue != None:  
    try:
      p = Place.objects.filter(venueid = venue)[0]
    except:
      p = Place(venueid=venue, location=l)
      try:
        p.save()
      except:
        transaction.rollback()
        print("An error has occured in saving the place\n")
      
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
       try:
         t.save()
         p.tags.add(t)
       except:
         transaction.rollback()
         print("An error has occured in saving the tag\n")
    return

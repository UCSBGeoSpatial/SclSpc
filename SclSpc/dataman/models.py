from django.contrib.gis.db import models
from django.utils.encoding import smart_str
from django.db import connection
from django.db.models import Count, F
from django.contrib.gis.geos import Point
import re
import datascrape.models
from datetime import datetime, timedelta

#User Model
#For tracking user movements by Name or Service UID
class User(models.Model):
	name = models.CharField(max_length=50, null=True)
	twitter_handle = models.CharField(max_length=50, null=True, blank=True)
	foursq_id = models.CharField(max_length=150, null=True, blank=True)

	def __unicode__(self):
		if self.name:
			return u'%s' % (self.name)
		else:
			return u'%s' % (self.twitter_handle)


#Location Model
#Many to Many relationship with CheckIns and Pics
class Location(models.Model):
	lon = models.FloatField()
	lat = models.FloatField()
	
	#GeoDjango Fields
	#Default SRID is WGS84
	point = models.PointField()
	objects = models.GeoManager()
	
	def __unicode__(self):
		return u'%s , %s' % (self.lon, self.lat)
	
	@classmethod	
	def overview_locations(cls):
		cursor = connection.cursor()
		cursor.execute("select st_astext(randompoint) as pt from RandomPoint((select geom from urban_areas where gid = 982))")
		row = cursor.fetchone()
		to_parse = str(row[0])
		coords = re.findall(r'\d+(?:\.\d*)?', to_parse)
		lon = float('-' + coords[0])
		lat = float(coords[1])
		p = Point(lon, lat)
		l = Location(lon = lon, lat = lat, point = p)
		return l
		

#Category Model
#For Foursquare and Twitter
class Category(models.Model):
	name = models.CharField(max_length=500)
	pluralName = models.CharField(max_length=500)
	shortName = models.CharField(max_length=500)
	fs_id = models.CharField(max_length=500)
	
	def __unicode__(self):
		return u'%s ' % (self.name)

#Place Model
#Didn't want venue information correlated to raw Lat/Lon Location
#Foursquare and Twitter info should be stored here
class Place(models.Model):
	location = models.ForeignKey(Location)
	
	name = models.CharField(max_length=500)
	venueid = models.CharField(max_length=255)
	
	foursq_id = models.CharField(max_length=255, null = True)
	foursq_primary_cat = models.ForeignKey(Category, related_name='fs_prime', null = True)
	foursq_categories = models.ManyToManyField(Category, null = True)
	twitter_handle = models.CharField(max_length=50, null=True, blank=True)
	
	@classmethod
	def top_places(cls):		
		#This is ranked by number of pics
		#Need to account for specific time delta
		return Place.objects.all().annotate(pic_count=Count('location__pic')).order_by('-pic_count') 
	
	def __unicode__(self):
		if self.name:
			return u'%s ' % (self.name)
		else:
			return u'%s ' % (self.venueid)
			
	def last_pic(self):
		pic = self.location.pic_set.all().order_by('created_at').reverse()[:1][0]
		return pic.url
		
	def inst_hour(self):
		count = self.location.pic_set.filter(created_at__gte = datetime.now() - timedelta(hours=2)).count()
		return count 
		
	def inst_today(self):
		count = self.location.pic_set.filter(created_at__gte = datetime.now() - timedelta(days=1)).count()
		return count 		
	
	def inst_ever(self):
		count = self.location.pic_set.all().count()
		return count
	
	def inst_with_delta(self, delta):
		picset = self.location.pic_set.filter(created_at__gte=datetime.now() - timedelta(hours = delta))
		return picset

	def lat(self):
		return self.location.lat

	def lon(self):
		return self.location.lon
		
#Tag Model
#Many to Many relationship with CheckIns and Pics	
class Tag(models.Model):
	content = models.CharField(max_length=50)
		
	def __unicode__(self):
		return u'%s ' % (self.content)
	
#CheckIn Model
#Has one Service, Has one Location, Has many Tags
class CheckIn(models.Model):
	location = models.ForeignKey(Location)
	place = models.ForeignKey(Place)
	user = models.ForeignKey(User)
	
	service = models.ForeignKey('datascrape.Service')
	
	message = models.CharField(max_length=255)
	uid = models.BigIntegerField()
	tags = models.ManyToManyField(Tag)
	created_at = models.DateTimeField()
	
	def __unicode__(self):
		return u'%s checkin: %i' % (self.service, self.id)
		
#Pic Model
#Has one Service, Has one Location, Has many Tags
class Pic(models.Model):
	service = models.ForeignKey('datascrape.Service', null=True)
	location = models.ForeignKey(Location)
	
	name = models.CharField(max_length=2400, null=True)
	tags = models.ManyToManyField(Tag, null=True)
	url = models.CharField(max_length=500)
	created_at = models.DateTimeField()
	
	def __unicode__(self):
		if self.name:
			return u'%s' % (self.name.replace("\n", ""))
		else:
			return u'picture - %s' % (self.service)
	
	def created(self):
		return self.created_at - timedelta(hours=8)
			
	def place(self):
		try:
			p = Place.objects.filter(location = self.location)[0]
			return p
		except:
			return False
	
	def category(self):
		if self.place():
			try:
				category = self.place().foursq_primary_cat
				return category
			except:
				return False
		else:
			return False
			
	
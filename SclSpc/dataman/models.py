from django.contrib.gis.db import models
from django.utils.encoding import smart_str

import datascrape.models

#User Model
#For tracking user movements by Name or Service UID
class User(models.Model):
	name = models.CharField(max_length=50, null=True)

	credentials = models.ManyToManyField('datascrape.ServiceInfo')

	def __unicode__(self):
		if self.name:
			return u'%s' % (self.name)
		else:
			return u'%s' % (self.uid)


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
	
	
#Place Model
#Didn't want venue information correlated to raw Lat/Lon Location
#Foursquare and Twitter info should be stored here
class Place(models.Model):
	location = models.ForeignKey(Location)
	
	name = models.CharField(max_length=500)
	venueid = models.CharField(max_length=255)
			
	def __unicode__(self):
		if self.name:
			return u'%s ' % (self.name)
		else:
			return u'%s ' % (self.venueid)
	
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
			
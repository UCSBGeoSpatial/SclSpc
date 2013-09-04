from django.contrib.gis.db import models

#Service Model
#Have to append to add APIKey, and Access Token fields
class Service(models.Model):
	name = models.CharField(max_length=50)
	
	#Returned when calling on object directly (no need to use name accessor)
	def __unicode__(self):
		return u'%s' % (self.name)

#User Model
#For tracking user movements by Name or Service UID
class User(models.Model):
	name = models.CharField(max_length=50, null=True)
	uid = models.BigIntegerField()
	userloc = models.CharField(max_length=500, null=True)
	
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
		if self.name:
			return u'%s' % (self.name)
		else:
			return u'%s , %s' % (self.lon, self.lat)
	
class Place(models.Model):
	location = models.ForeignKey(Location)
	
	placeid = models.CharField(max_length=255)
	placename = models.CharField(max_length=500)
	placeurl = models.CharField(max_length=500)
	
	def __unicode__(self):
		return u'%s ' % (self.placename)
	
#Tag Model
#Many to Many relationship with CheckIns and Pics	
class Tag(models.Model):
	content = models.CharField(max_length=50)
	
	def __unicode__(self):
		return content
	
#CheckIn Model
#Has one Service, Has one Location, Has many Tags
class CheckIn(models.Model):
	location = models.ForeignKey(Location)
	place = models.ForeignKey(Place)
	
	service = models.ForeignKey(Service)
	message = models.CharField(max_length=255)
	uid = models.BigIntegerField()
	tags = models.ManyToManyField(Tag)
	created_at = models.DateTimeField()
	
	def __unicode__(self):
		return u'%s checkin: %i' % (self.service, self.id)
		
#Pic Model
#Has one Service, Has one Location, Has many Tags
class Pic(models.Model):
	service = models.ForeignKey(Service)
	location = models.ForeignKey(Location)
	name = models.CharField(max_length=50, null=True)
	tags = models.ManyToManyField(Tag)
	url = models.CharField(max_length=100)
	created_at = models.DateTimeField()
	
	def __unicode__(self):
		if self.name:
			return u'%s' % (self.name)
		else:
			return "picture" + self.service + " " + self.created_at
			return u'picture - %s %s' % (self.service, self.created_at)
			
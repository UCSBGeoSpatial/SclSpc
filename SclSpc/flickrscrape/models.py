from django.db import models
from django.db import transaction, IntegrityError
from dataman.models import Location, Tag, Pic
from django.contrib.gis.geos import Point
from datetime import datetime

import flickrapi

#Flickr Interface
#Flickr API info
class FlickrInterface(models.Model):
	uid = models.BigIntegerField(null=True)
	access_key = models.CharField(max_length=150, null=True)
	shared_secret = models.CharField(max_length=150, null=True)

	def __unicode__(self):
		return u'Flickr auth'

	def _flickr_interface(self):
		flickr = flickrapi.FlickrAPI(self.access_key)
		return flickr

	def test_query(self):
		f = self._flickr_interface()
		photos = f.photosets_getList(user_id = '57731761@N05', per_page = '10')
		test_pho = photos.find('photosets').findall('photoset')[0]
		return u'%s : %s' % (test_pho.find('title').text, test_pho.find('description').text)
	
	
	#This method will return a list of photos within 32km of a Location object
	# def test_geo(self, location):
	def test_geo(self):
		
		all_locations = Location.objects.all()
		seed = all_locations[randrange(len(all_locations))]
		lat = seed.lat
		lon = seed.lon
		rad = 32    
		
		f = self._flickr_interface()
		photos = f.photos_search(lat = str(lat), lon = str(lon), rad = str(rad), extras = 'geo, tags, url_l, date_taken', per_page = '100')
		
		thelist = photos.find('photos').findall('photo')
		
		return thelist
		
	def save_geo(self):
		thelist = self.test_geo()
		for photo in thelist:
			try:
				title = photo.attrib['title']
				tags = photo.attrib['tags'].split(' ')
				url = photo.attrib['url_l']
				latitude = float(photo.attrib['latitude'])
				longitude = float(photo.attrib['longitude'])
				
				#Location check
				l = self.parse_location(latitude, longitude)
				
				#Pic check
				if url:
					try:
						c_at = datetime.strptime(photo.attrib['datetaken'], "%Y-%m-%d %H:%M:%S")
						self.parse_pic(title, l, url, c_at, tags)		
					except:
						continue
			
			except KeyError:
				continue
					
		return thelist
	
	def parse_pic(self, title, l, url_l, c_at, tags):
		
		try:
			p = Pic.objects.filter(url = url_l)[0]
		except:
			p = Pic(name = title, location = l, url = url_l, created_at = c_at)
			try:
				p.save()
				self.parse_tags(p, tags)
			except IntegrityError:
				transaction.rollback()
				print("An error has occured in saving the picture\n")
		return p
	
	def parse_location(self, latitude, longitude):
		#checks for existing location
		l = Location.objects.filter(lon = longitude, lat = latitude)
		if l:
			l = l[0]
		#if location doesn't exist
		else:
			pnt = Point(longitude, latitude)
			l = Location(lon = longitude, lat = latitude, point = pnt)
			if l.save():
				print "Location Saved\n"
		
		return l
	
	def parse_tags(self, p, tags):
		#Cycles thru picture tags
		for tag in tags:
			print tag
			try:
				t = Tag.objects.filter(content = tag)[0]
				
			except:
				t = Tag(content = tag)
				t.save()
								
			p.tags.add(t)
				
		return p.tags
	
	


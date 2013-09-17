from django.db import models
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
		lat = 34.050238
		lon = -118.244828
		rad = 32
		f = self._flickr_interface()
		
		photos = f.photos_search(lat = str(lat), lon = str(lon), rad = str(rad), extras = 'geo, tags, url_l, date_taken')
		
		thelist = photos.find('photos').findall('photo')
		
		return thelist
		
	def save_geo(self):
		lat = 34.050238
		lon = -118.244828
		rad = 32
		f = self._flickr_interface()
		
		photos = f.photos_search(lat = str(lat), lon = str(lon), rad = str(rad), extras = 'geo, tags, url_l, date_taken', per_page = '100')
		
		thelist = photos.find('photos').findall('photo')
		
		for photo in thelist:
			try:
				title = photo.attrib['title']
				tags = photo.attrib['tags'].split(' ')
				url = photo.attrib['url_l']
				latitude = float(photo.attrib['latitude'])
				longitude = float(photo.attrib['longitude'])
				c_at = datetime.strptime(photo.attrib['datetaken'], "%Y-%m-%d %H:%M:%S")
			except KeyError:
				continue
				
			#Need to add GEOPOINT object creation to fill point field
			pnt = Point(longitude, latitude)
			l = Location(lon = longitude, lat = latitude, point = pnt)
			if l.save():
				print "Location Saved\n"
			
			#Need to see if this is a legal way to set location foreign key
			p = Pic(name = title, location = l, created_at = c_at)
			if url:
				p.url = url
			if p.save():
				print "Pic Saved\n"
			if tags:
				for tag in tags:
					print tag
					t = Tag(content = tag)
					if t.save():
						print "Tag Saved\n"
		return thelist
	
	#I'm using this to test.
	#It takes the list returned from test_geo and prints
	#the Title and the URL
	# def print_data(self, thelist):
	# 	for photo in thelist:
	# 		try:
	# 			title = photo.attrib['title']
	# 			tags = photo.attrib['tags']
	# 			url = photo.attrib['url_l']
	# 			latitude = photo.attrib['latitude']
	# 			longitude = photo.attrib['longitude']
	# 			created_at = photo.attrib['date_taken']
	# 		except KeyError:
	# 			continue
	# 			
	# 		print title + ' ' + url
		
	#Need to test this.
	#Should create new photo and location objects	
	# def save_data(self, thelist):
	# 	for photo in thelist:
	# 		try:
	# 			title = photo.attrib['title']
	# 			tags = photo.attrib['tags'].split
	# 			url = photo.attrib['url_l']
	# 			latitude = float(photo.attrib['latitude'])
	# 			longitude = float(photo.attrib['longitude'])
	# 			c_at = photo.attrib['date_taken']
	# 		except KeyError:
	# 			continue
	# 			
	# 		if latitude and longitude and title:
	# 			#Need to add GEOPOINT object creation to fill point field
	# 			pnt = Point(longitude, latitude)
	# 			l = Location(lon = longitude, lat = latitude, point = pnt, created_at = c_at)
	# 			l.save()
	# 			
	# 			#Need to see if this is a legal way to set location foreign key
	# 			p = Pic(name = title, location = l)
	# 			if url:
	# 				p.url = url
	# 			p.save()
	# 		if tags:
	# 			for tag in tags:
	# 				t = Tag(content = tag)
	# 				t.save()
	# 			

	# def geo_query(self, Location):


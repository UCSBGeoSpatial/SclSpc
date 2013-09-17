from django.db import models
from dataman.models import Location
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
		
		photos = f.photos_search(lat = str(lat), lon = str(lon), rad = str(rad), extras = 'geo, tags, url_l ')
		
		thelist = photos.find('photos').findall('photo')
		
		return thelist
	
	#I'm using this to test.
	#It takes the list returned from test_geo and prints
	#the Title and the URL
	def print_data(self, thelist):
		for photo in thelist:
			try:
				title = photo.attrib['title']
				tags = photo.attrib['tags']
				url = photo.attrib['url_l']
				latitude = photo.attrib['latitude']
				longitude = photo.attrib['longitude']
			except KeyError:
				continue
				
			print title + ' ' + url
		
	#Need to test this.
	#Should create new photo and location objects	
	def save_data(self, thelist):
		for photo in thelist:
			try:
				title = photo.attrib['title']
				tags = photo.attrib['tags']
				url = photo.attrib['url_l']
				latitude = photo.attrib['latitude']
				longitude = photo.attrib['longitude']
			except KeyError:
				continue
				
			if latitude && longitude && title:
				

	# def geo_query(self, Location):


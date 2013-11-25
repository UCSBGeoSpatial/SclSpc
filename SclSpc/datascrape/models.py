from django.db import models
import flickrapi

#Service Model
#Have to append to add APIKey, and Access Token fields
class Service(models.Model):
	name = models.CharField(max_length=50)
	
	#Returned when calling on object directly (no need to use name accessor)
	def __unicode__(self):
		return u'%s' % (self.name)
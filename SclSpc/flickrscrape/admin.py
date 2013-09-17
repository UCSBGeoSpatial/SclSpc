from django.contrib.gis import admin
from models import FlickrInterface

#Defines which models are accessible via Admin interface
#gis.admin allows java slippy map :D
admin.site.register(FlickrInterface, admin.GeoModelAdmin)
from django.contrib.gis import admin
from models import FoursquareInterface

#Defines which models are accessible via Admin interface
#gis.admin allows java slippy map :D
admin.site.register(FoursquareInterface, admin.GeoModelAdmin)
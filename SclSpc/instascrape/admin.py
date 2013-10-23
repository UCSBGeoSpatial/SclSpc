from django.contrib.gis import admin
from models import InstagramInterface

#Defines which models are accessible via Admin interface
#gis.admin allows java slippy map :D
admin.site.register(InstagramInterface, admin.GeoModelAdmin)
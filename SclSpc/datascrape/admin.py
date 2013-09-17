from django.contrib.gis import admin
from models import Service, ServiceInfo

#Defines which models are accessible via Admin interface
#gis.admin allows java slippy map :D
admin.site.register(Service, admin.GeoModelAdmin)
admin.site.register(ServiceInfo, admin.GeoModelAdmin)
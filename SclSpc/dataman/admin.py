from django.contrib.gis import admin
from models import Location, Pic, CheckIn, Place, Tag

#Defines which models are accessible via Admin interface
#gis.admin allows java slippy map :D
admin.site.register(Location, admin.GeoModelAdmin)
admin.site.register(Pic, admin.GeoModelAdmin)
admin.site.register(CheckIn, admin.GeoModelAdmin)
admin.site.register(Place, admin.GeoModelAdmin)
admin.site.register(Tag, admin.GeoModelAdmin)
from django.contrib.gis import admin
from models import Location, Pic, CheckIn, Place, Tag, Category

class PicAdmin(admin.ModelAdmin):
  
  list_display = ('name', 'place', 'category', 'created')
  ordering = ('-created_at',)

class PlaceAdmin(admin.ModelAdmin):
  list_display = ('name', 'foursq_primary_cat')
  ordering = ('foursq_primary_cat',)
  list_filter = ('foursq_primary_cat',)

#Defines which models are accessible via Admin interface
#gis.admin allows java slippy map :D
admin.site.register(Location, admin.GeoModelAdmin)
admin.site.register(Pic, PicAdmin)
admin.site.register(CheckIn, admin.GeoModelAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Tag, admin.GeoModelAdmin)
admin.site.register(Category, admin.GeoModelAdmin)
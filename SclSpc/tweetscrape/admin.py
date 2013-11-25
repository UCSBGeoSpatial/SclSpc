from django.contrib.gis import admin
from models import TwitterInterface

#Defines which models are accessible via Admin interface
#gis.admin allows java slippy map :D
admin.site.register(TwitterInterface, admin.ModelAdmin)
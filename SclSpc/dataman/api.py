from models import Place
from restless.models import serialize
from restless.views import Endpoint
from django.db.models import Count, Q

class GetNightlifeList(Endpoint):
	def get(self, request):
		venues_list = Place.objects.filter(Q(foursq_primary_cat__name__contains='Bar')|Q(foursq_primary_cat__name__contains='Lounge')|Q(foursq_primary_cat__name__contains='Beer')).annotate(pic_count=Count('location__pic')).order_by('pic_count').reverse()[:10]
		fields = ('id', 'name', 'pic_count',
			('foursq_primary_cat', dict(
				fields = [
					'name',
				]
				)),
			('location', dict(
				fields = [
					'lat',
					'lon'
				]
				))
			)
		return serialize(venues_list, fields)

class GetVenueList(Endpoint):
	def get(self, request):
		venues_list = Place.objects.all().annotate(pic_count=Count('location__pic')).annotate(preview='location__pic').order_by('pic_count').reverse()[:10]
		fields = ('id', 'name', 'pic_count',
			('foursq_primary_cat', dict(
				fields = [
					'name',
				]
				)),
			('location', dict(
				fields = [
					'lat',
					'lon'
				]
				))
			)
		return serialize(venues_list, fields)
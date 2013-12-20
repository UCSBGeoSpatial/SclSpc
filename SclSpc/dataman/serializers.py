from rest_framework import serializers

class PlaceSerializer(serializers.Serializer):
	pk = serializers.Field()
	name = serializers.CharField(max_length=500)
	foursq_primary_cat = serializers.CharField(max_length=500)
	foursq_categories = serializers.RelatedField(many=True)
	last_pic = serializers.CharField(max_length=500)
	lat = serializers.FloatField()
	lon = serializers.FloatField()

class PicSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=2400)
	tags = serializers.RelatedField(many=True)
	url = serializers.CharField(max_length=500)
	created_at = serializers.DateTimeField()
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q, Count
from django.core import serializers
from models import Pic, Place
from serializers import PlaceSerializer, PicSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 

class PlaceList(APIView):
  """
  List All Places
  """
  def get(self, request, format=None):
    places = Place.objects.filter(Q(foursq_primary_cat__name__contains='Bar')|Q(foursq_primary_cat__name__contains='Lounge')|Q(foursq_primary_cat__name__contains='Beer')).annotate(pic_count=Count('location__pic')).order_by('pic_count').reverse()[:10]
    #places = Place.objects.all()
    serializer = PlaceSerializer(places, many=True)
    return Response(serializer.data)

class PlaceDetail(APIView):
  """
  Retrieve, update or delete a snippet instance.
  """
  def get_object(self, pk):
      try:
          return Place.objects.get(id=pk)
      except Place.DoesNotExist:
          raise Http404

  def get(self, request, pk, format=None):
      place = self.get_object(pk)
      serializer = PlaceSerializer(place)
      return Response(serializer.data)

class PlacePic(APIView):
  """
  Retrieve all pics related to a place
  """

  def get_object(self, pk):
    try:
      return Place.objects.get(id=pk).location.pic_set.all()
    except Place.DoesNotExist:
      raise Http404

  def get(self, request, pk, format=None):
    pic_list = self.get_object(pk)
    serializer = PicSerializer(pic_list, many=True)
    return Response(serializer.data)

# def index(request):
#   pics_list = Pic.objects.filter(location__place__name__isnull = False).exclude(location__place__name = '0').order_by('created_at').reverse()[:100]
#   paginator = Paginator(pics_list, 10)
#   page = request.GET.get('page')
#   try:
#     show_lines = paginator.page(page)
#   except PageNotAnInteger:
#     show_lines = paginator.page(1)
#   except EmptyPage:
#     show_lines = paginator.page(paginator.num_pages)
#   return render_to_response('index.html', RequestContext(request, {'pics_list': show_lines}))

# def categories(request):
#   pics_list = Pic.objects.filter(location__place__foursq_primary_cat__isnull = False).order_by('created_at').reverse()[:100]
#   paginator = Paginator(pics_list, 10)
#   page = request.GET.get('page')
#   try:
#     show_lines = paginator.page(page)
#   except PageNotAnInteger:
#     show_lines = paginator.page(1)
#   except EmptyPage:
#     show_lines = paginator.page(paginator.num_pages)
#   return render_to_response('categories.html', RequestContext(request, {'pics_list': show_lines}))
  
# def nightlife(request):
#   pics_list = Pic.objects.filter(Q(location__place__foursq_primary_cat__name__contains='Bar') | 
#                                                 Q(location__place__foursq_primary_cat__name__contains='Lounge') |
#                                                 Q(location__place__foursq_primary_cat__name__contains='Beer')).order_by('created_at').reverse()[:100]
#   paginator = Paginator(pics_list, 10)
#   page = request.GET.get('page')
#   try:
#     show_lines = paginator.page(page)
#   except PageNotAnInteger:
#     show_lines = paginator.page(1)
#   except EmptyPage:
#     show_lines = paginator.page(paginator.num_pages)
#   return render_to_response('nightlife.html', RequestContext(request, {'pics_list': show_lines}))
  
    
# def venue(request, venue_id):
#   v = Place.objects.get(id=venue_id)
#   pics = v.pics(limit = 100)
#   paginator = Paginator(pics, 4)
#   page = 1
#   try:
#     show_lines = paginator.page(page)
#   except PageNotAnInteger:
#     show_lines = paginator.page(1)
#   except EmptyPage:
#     show_lines = paginator.page(paginator.num_pages)
#   return render_to_response('venue.html', RequestContext(request, {'venue': v, 'pics_list': show_lines}))
  
# def venue_json(request, venue_id):
#   v = Place.objects.get(id=venue_id)
#   pics = v.location.pic_set.all().order_by('created_at').reverse()[:100]
#   paginator = Paginator(pics, 10)
#   page = request.GET.get('page')
#   try:
#     show_lines = paginator.page(page)
#   except PageNotAnInteger:
#     show_lines = paginator.page(1)
#   except EmptyPage:
#     show_lines = paginator.page(paginator.num_pages)
    
#   data = serializers.serialize('json', show_lines)
  
#   return HttpResponse(data, mimetype='application/json')
    
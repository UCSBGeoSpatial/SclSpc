from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q, Count
from restless.views import Endpoint
from django.core import serializers
from models import Pic, Place


def index(request):
  pics_list = Pic.objects.filter(location__place__name__isnull = False).exclude(location__place__name = '0').order_by('created_at').reverse()[:100]
  paginator = Paginator(pics_list, 10)
  page = request.GET.get('page')
  try:
    show_lines = paginator.page(page)
  except PageNotAnInteger:
    show_lines = paginator.page(1)
  except EmptyPage:
    show_lines = paginator.page(paginator.num_pages)
  return render_to_response('index.html', RequestContext(request, {'pics_list': show_lines}))

def categories(request):
  pics_list = Pic.objects.filter(location__place__foursq_primary_cat__isnull = False).order_by('created_at').reverse()[:100]
  paginator = Paginator(pics_list, 10)
  page = request.GET.get('page')
  try:
    show_lines = paginator.page(page)
  except PageNotAnInteger:
    show_lines = paginator.page(1)
  except EmptyPage:
    show_lines = paginator.page(paginator.num_pages)
  return render_to_response('categories.html', RequestContext(request, {'pics_list': show_lines}))
  
def nightlife(request):
  pics_list = Pic.objects.filter(Q(location__place__foursq_primary_cat__name__contains='Bar') | 
                                                Q(location__place__foursq_primary_cat__name__contains='Lounge') |
                                                Q(location__place__foursq_primary_cat__name__contains='Beer')).order_by('created_at').reverse()[:100]
  paginator = Paginator(pics_list, 10)
  page = request.GET.get('page')
  try:
    show_lines = paginator.page(page)
  except PageNotAnInteger:
    show_lines = paginator.page(1)
  except EmptyPage:
    show_lines = paginator.page(paginator.num_pages)
  return render_to_response('nightlife.html', RequestContext(request, {'pics_list': show_lines}))
  
    
def venue(request, venue_id):
  try:
    v = Place.objects.get(id=venue_id)
    pics = v.pics(limit = 100)
    paginator = Paginator(pics, 4)
    page = request.Get.get('page')
    try:
      show_lines = paginator.page(page)
    except PageNotAnInteger:
      show_lines = paginator.page(1)
    except EmptyPage:
      show_lines = paginator.page(paginator.num_pages)
  except:
    raise Http404
  return render_to_response('venue.html', RequestContext(request, {'venue': v, 'pics_list': show_lines}))
  
def venue_json(request, venue_id):
  v = Place.objects.get(id=venue_id)
  pics = v.location.pic_set.all().order_by('created_at').reverse()[:100]
  paginator = Paginator(pics, 10)
  page = request.GET.get('page')
  try:
    show_lines = paginator.page(page)
  except PageNotAnInteger:
    show_lines = paginator.page(1)
  except EmptyPage:
    show_lines = paginator.page(paginator.num_pages)
    
  data = serializers.serialize('json', show_lines)
  
  return HttpResponse(data, mimetype='application/json')
    
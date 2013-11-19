from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.context import RequestContext
from django.shortcuts import render_to_response

from models import Pic
# Create your views here.

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
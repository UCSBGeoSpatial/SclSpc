from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.context import RequestContext
from django.shortcuts import render_to_response

from models import Pic
# Create your views here.

def index(request):
  pics_list = Pic.objects.all()[:1000]
  context = { 'pics_list' : pics_list }
  return render(request, 'index.html', context)

def categories(request):
  pics = Pic.objects.all()[:100]
  pics_list = []
  for pic in pics:
    if pic.category():
      pics_list.append(pic)
  paginator = Paginator(pics_list, 10)
  page = request.GET.get('page')
  try:
    show_lines = paginator.page(page)
  except PageNotAnInteger:
    show_lines = paginator.page(1)
  except EmptyPage:
    show_lines = paginator.page(paginator.num_pages)
  return render_to_response('categories.html', RequestContext(request, {'pics_list': show_lines}))
from django.http import HttpResponse
from django.shortcuts import render
from models import Pic
# Create your views here.

def index(request):
  pics_list = Pic.objects.all()
  context = { 'pics_list' : pics_list }
  return render(request, 'index.html', context)
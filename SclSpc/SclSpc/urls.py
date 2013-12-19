from django.conf.urls import patterns, include, url
from django.contrib.gis import admin
from dataman import views
from dataman.api import GetNightlifeList, GetVenueList

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SclSpc.views.home', name='home'),
    # url(r'^SclSpc/', include('SclSpc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name = 'index'),
    url(r'^categories$', views.categories, {}, 'categories'),
    url(r'^nightlife$', views.nightlife, {}, 'nightlife'),
    url(r'^nightlife_json$', GetNightlifeList.as_view()),    
    url(r'^venue_list$', GetVenueList.as_view()),
    url(r'^venue/(\d+)/$', views.venue, {}, 'venue'),
    url(r'^venue_json/(\d+)/$', views.venue_json, {}, 'venue_json')
)

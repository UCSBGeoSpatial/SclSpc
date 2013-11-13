from django_cron import CronJobBase, Schedule
from fourscrape.models import FoursquareInterface

class catScrape(CronJobBase):
  RUN_EVERY_MINS = 240 #every 4 hours
  schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
  code = 'fourscrape.catScrape'
  def do(self):
    fs = FoursquareInterface.objects.all()[0]
    try:
      fs.place_scrape()
    except Exception, error:
      print "An error has occured in while scraping places!"
      print str(error)
from django_cron import CronJobBase, Schedule
from instascrape.models import InstagramInterface
from random import randrange

class overviewScrape(CronJobBase):
  RUN_EVERY_MINS = 180 #every 3 hours
  schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
  code = 'instascrape.overviewScrape'
  def do(self):
    all_inst = InstagramInterface.objects.all()
    inst = all_inst[randrange(len(all_inst))]
    for i in range(0,2000):
      try:
        inst.overview_scrape()
      except Exception, error:
        print "An error has occured in the scrape loop!"
        print str(error)
        
class placeScrape(CronJobBase):
  RUN_EVERY_MINS = 120 #every 2 hours
  schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
  code = 'instascrape.placeScrape'
  def do(self):
    all_inst = InstagramInterface.objects.all()
    inst = all_inst[randrange(len(all_inst))]
    try:
      inst.place_scrape()
    except Exception, error:
      print "An error has occured in while scraping places!"
      print str(error)
from django_cron import CronJobBase, Schedule
from instascrape.models import InstagramInterface

class overviewScrape(CronJobBase):
  RUN_EVERY_MINS = 120 #every hour
  schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
  code = 'instascrape.overviewScrape'
  def do(self):
    inst = InstagramInterface.objects.all()[0]
    for i in range(0,4999):
      try:
        photos = inst.overview_scrape()
      except:
        print "An error has occured in saving pics"
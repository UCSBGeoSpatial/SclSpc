from django_cron import cronScheduler, Job
import logging
#This function runs the overview scrape every hour
from instascrape import InstagramInterface

class overviewScrape(Job):  
  #run every hour (in seconds)
  run_every = 3600

  def job(self):
    #instantiate logger
    logger = logging.getLogger('SclSpc.instascrape')
    
    #grab the first API keypair
    inst = InstagramInterface.objects.all()[0]
    
    #try to run 5000 overview scrapes
    for i in range(0, 5000):
      photos = inst.overview_scrape()
      try:
        inst.save_pics(photos)
      except:
        logger.error('save_pics has failed')
        logger.exception()
        
cronScheduler.register(overviewScrape)
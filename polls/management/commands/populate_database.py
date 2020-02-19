from polls.datscript2 import Data
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'site', type=str, help='The site which is being scraped'
        )

    def handle(self, *args, **kwargs):
        site = kwargs['site']
        pop = Data()
        Data.clear()
        pop.scrape(site)
        pop.populate()

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webscrape_project.settings")

# your imports, e.g. Django models
from polls import models

# From now onwards start your script..

if __name__ == '__main__':
    p = models.Product()
    p.type = 'test1'
    p.brand = 'test2'
    p.name = 'test3'
    p.price = 'test4'
    p.site = 'test.com'
    p.save()

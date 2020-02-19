from django.contrib import admin
from polls.models import Product

from django.views.generic import ListView
from polls.models import Product

# Register your models here.
admin.site.register(Product)


class ContactsList(ListView):
    paginate_by = 2
    model = Product


admin.site.site_header = 'Part Ninja Administration'


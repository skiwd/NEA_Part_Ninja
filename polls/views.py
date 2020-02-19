from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator


# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView, ListView
from .models import Product
from django import forms

def is_valid_queryparam(param):
    return param != '' and param is not None


def index(request):
    qs = Product.objects.all()
    paginator = Paginator(qs, 25)  # Show 25 products per page
    page = request.GET.get('page')
    qspage = paginator.get_page(page)


    brands = Product.objects.all().values_list('brand', flat=True).distinct()
    brands = brands.order_by('brand')
    sorting = request.GET.get('sort')
    search = request.GET.get('search')
    type_filter = request.GET.get('type')
    brand_filter = request.GET.get('brand')

    if is_valid_queryparam(search):
        qs = qs.filter(name__icontains=search)

    if is_valid_queryparam(type_filter) and type_filter != 'Any':
        qs = qs.filter(type__icontains=type_filter.lower())

    if is_valid_queryparam(brand_filter) and brand_filter != 'Any':
        qs = qs.filter(brand__exact=brand_filter)

    if is_valid_queryparam(sorting):
        if sorting == 'Price Ascending':
            qs = qs.order_by('price')
        elif sorting == 'Price Descending':
            qs = qs.order_by('-price')
        elif sorting == 'Relevance':
            qs = qs.order_by('?')

    if 'overclockers' in request.GET:
        print('overclockers')

    count = len(qs)

    context = {
        'queryset': qs,
        'brands': brands,
        'count': count,
    }
    return render(request, "polls/index.html", context)


def detail(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        # link = list(product)[5]
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    return render(request, 'polls/detail.html', {'product': product})

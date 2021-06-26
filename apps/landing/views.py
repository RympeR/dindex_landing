from django.shortcuts import render
import requests
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaulttags import register


@register.filter
def get_range(value):
    return range(value)

def index(request):
    url = 'https://dindex.site/index/index/getValues'
    data = requests.get(url)
    page = int(request.GET.get('page', 1))
    data = data.json()['data']
    keys = list(data.keys())
    data = data[keys[page-1]]
    context = {'data':data, 'pages': len(keys), 'current_page': page}
    return render(request, 'index.html', context=context)
 
from django.shortcuts import render
import requests
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaulttags import register
import numpy as np
from plotly.offline import plot
import plotly.graph_objects as go


@register.filter
def get_range(value):
    return range(1, value)

def index(request):
    def scatter():
        x1 = [1,2,3,4]
        y1 = [30, 35, 25, 45]
        
        trace = go.Scatter(
            x=x1,
            y=y1,
            visible=True,
            opacity=0.6,
            mode='markers',
        )
        layout = dict(
            title='Simple graph',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis=dict(range=[min(y1), max(y1)]),
        )

        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        return plot_div
    url = 'https://dindex.site/index/index/getValues'
    data = requests.get(url)
    page = int(request.GET.get('page', 1))
    data = data.json()['data']
    # keys = list(filter(lambda x: int(x.split("-")[0])>=2019 ,list(data.keys())))
    keys = list(data.keys())
    # data = sorted(data[keys[ -1]], key=lambda x: float(x['weight']))
    data = data[keys[-1]]
    print(len(data))
    data = sorted(data, key=lambda x: float(x['weight']))[::-1]
    data = np.array_split(data, 10) 
    context = {'data':data, 'pages': len(keys), 'current_page': page, 'plot' : scatter(), 'zip': zip}
    return render(request, 'index.html', context=context)

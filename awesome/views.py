
import numpy as np
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure
from django.http import HttpResponse
from django.shortcuts import render_to_response
import json

from awesome.converter import scatter_to_base64
from awesome.tasks import generate_and_save_graph_image
from awesome.models import Graph

def df_view(request):
    array = np.random.random((10, 10))
    df = pd.DataFrame(array)
    return HttpResponse(df.to_html())


def graph_view_matplot_lib(request):
    graph_one = scatter_to_base64(([1, 2, 3, 4], [10, 1, 5, 3]))
    graph_two = scatter_to_base64(([1, 2, 3, 4], [1, 1, 1, 5]))
    return render_to_response("base.html", {"graph_one": graph_one, "graph_two": graph_two})


def bokeh_graph_view(request):
    plot = figure()
    if request.GET:
        x_data = json.loads(request.GET.get("x"))
        y_data = json.loads(request.GET.get("y"))

    else:
        x_data, y_data = ([1, 2, 3, 4], [10, 1, 5, 3])

    plot.line(x_data, y_data)
    script, div = components(plot)
    generate_and_save_graph_image.delay()
    return render_to_response("base.html", {"bokeh_script": script, "bokeh_graph": div})

#  ^^^^^ NO URLS FOR THE ABOVE VIEWS ^^^^^  #


def graph_view(request):
    if request.GET:
        x_data = json.loads(request.GET.get("x"))
        y_data = json.loads(request.GET.get("y"))
    else:
        x_data, y_data = ([1, 2, 3, 4], [10, 1, 5, 3])

    graph_data = [x_data, y_data]

    graph = Graph.objects.filter(data=str(graph_data))
    if not graph:
        graph_content = scatter_to_base64(graph_data)
        generate_and_save_graph_image.delay(graph_data)
    else:
        graph_content = graph.get().content

    return render_to_response("base.html", {"graph": graph_content})


def graph(request):
    if request.GET:
        x_data = json.loads(request.GET.get("x"))
        y_data = json.loads(request.GET.get("y"))
    else:
        x_data, y_data = ([1, 2, 3, 4], [10, 1, 5, 3])

    graph_data = [x_data, y_data]
    graph_content = scatter_to_base64(graph_data)
    object = {"image_source": graph_content}
    generate_and_save_graph_image.delay(graph_data)
    return HttpResponse(json.dumps(object), content_type="application/json")

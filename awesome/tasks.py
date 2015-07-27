from awesome.converter import scatter_to_base64
from graphz.celery_app import app

from awesome.models import Graph
import time


@app.task
def generate_and_save_graph_image(data):
    time.sleep(10)
    base64_string = scatter_to_base64(data)
    Graph.objects.create(content=base64_string, data=str(data))
    return True
from django.db import models

# Create your models here.

class Graph(models.Model):
    content = models.TextField()
    data = models.TextField(db_index=True)
from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=120)
    titlee = models.CharField(max_length=120, default='text')
    titleee = models.CharField(max_length=120, default='text')
    titleeee = models.CharField(max_length=120, default='text')

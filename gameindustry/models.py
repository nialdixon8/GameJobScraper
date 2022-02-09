from django.db import models


class Offer(models.Model):
    title = models.CharField(max_length=50)
    employer = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    requirements = models.CharField(max_length=50)

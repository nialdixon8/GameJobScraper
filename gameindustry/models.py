from django.db import models


class Offer(models.Model):
    """Corresponds to essential fields stored in the SQL database."""
    """Generally each model corresponds to a table in the database."""
    title = models.CharField(max_length=50)
    employer = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    requirements = models.CharField(max_length=50)

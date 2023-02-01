"""This module contains models for database"""

from django.db import models


class CountdownInfo(models.Model):
    """Used to store the countdown information"""

    title = models.CharField(max_length=100)
    timestamp = models.CharField(max_length=20)
    uri = models.CharField(max_length=10)

    def __str__(self):
        return self.uri + ":" +self.title

from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    expected_participants = models.IntegerField()
    seats_left = models.IntegerField()
    poster_url = models.URLField(blank=True)
    registration_link = models.URLField(blank=True)

    def __str__(self):
        return self.name

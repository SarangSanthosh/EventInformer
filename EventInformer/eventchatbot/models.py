from django.db import models
from firebase.fire import store_event_in_firebase  

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

  
    def save(self, *args, **kwargs):
       
        super(Event, self).save(*args, **kwargs)

        event_data = {
            'name': self.name,
            'description': self.description,
            'date': str(self.date),  
            'time': str(self.time),  
            'location': self.location,
            'expected_participants': self.expected_participants,
            'seats_left': self.seats_left,
            'poster_url': self.poster_url,
            'registration_link': self.registration_link
        }

      
        store_event_in_firebase(event_data)

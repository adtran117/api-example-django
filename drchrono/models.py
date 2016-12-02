# from django.db import models
from mongoengine import *
connect('drchrono2')

# Create your models here.
class Appointment(Document):
  appointment_id = StringField()
  # I use string field for time because I had trouble parsing date time to a string
  time_checkedin = StringField()
  time_ready = StringField()
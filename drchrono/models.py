# from django.db import models
from mongoengine import *

# Create your models here.
class Appointment(EmbeddedDocument):
  time_checkedin = DateTimeField()
  time_stop = DateTimeField()

class Patient(Document):
  patient_id = StringField()
  first_name = StringField()
  last_name = StringField()
  appointments = ListField(EmbeddedDocumentField(Appointment))
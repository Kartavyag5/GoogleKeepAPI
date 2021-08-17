from django.db import models
from django.contrib.auth import User

class Notes(models.Model):
    Name = models.CharField(max_length=50)

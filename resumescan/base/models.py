from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Cvuploads(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_description = models.TextField(null=True)
    file = models.FileField(null=True)

    
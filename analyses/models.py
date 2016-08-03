from django.db import models
from bioinfo_biobureau.users.models import User

from projects.models import Project

# Create your models here.
class Analysis(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=255)
    description = models.TextField()
    analysis_type = models.TextField()


class Machine(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    details = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True)


class Task(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    instance_type = models.CharField(max_length=255)
    details = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True)



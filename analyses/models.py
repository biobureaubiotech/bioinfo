from django.db import models

from django.contrib.postgres.fields import JSONField
from bioinfo_biobureau.users.models import User

from projects.models import Project

# Create your models here.
class Analysis(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=255)
    description = models.TextField()
    analysis_type = models.TextField()
    parameters = JSONField()

    status = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True)

    started = models.DateTimeField(null=True)
    finished = models.DateTimeField(null=True)
    time_taken = models.TimeField(null=True)

class Instance(models.Model):

    analysis = models.ForeignKey(Analysis)
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)

    instance_id = models.TextField()
    ip_address = models.TextField()
    status = models.TextField()
    
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True)

    started = models.DateTimeField(null=True)
    finished = models.DateTimeField(null=True)
    

# class Task(models.Model):
#     name = models.CharField(max_length=255)
#     user = models.ForeignKey(User)
#     instance_type = models.CharField(max_length=255)
#     details = models.TextField()
#     created_date = models.DateTimeField(auto_now_add=True, editable=False)
#     modified_date = models.DateTimeField(auto_now=True)
#     
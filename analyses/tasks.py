from celery.decorators import task
from django.conf import settings

from analyses.models import Analysis

@task(name="start_analysis")
def StartAnalysis(analysis_id):
    print('Finished!')
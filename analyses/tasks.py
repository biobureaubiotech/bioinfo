from celery.decorators import task
from django.conf import settings

import zipfile

@task(name="turn_on_machine")
def turn_on_machine(project_id):
    print('Finished!')

from __future__ import absolute_import
import os
from celery import Celery
from django.apps import AppConfig
from django.conf import settings


app = Celery('bioinfo_biobureau')


# @app.task(bind=True)
# def debug_task(self):
#     print('HELLO TASK!!!')
#     print('Request: {0!r}'.format(self.request))  # pragma: no cover

@app.task()
def test_task(self):
    print('##########################Foo#################')
    sleep(4)
    print('###########################################')
    sleep(2)
    print('##########################Bar#################')
    return 3
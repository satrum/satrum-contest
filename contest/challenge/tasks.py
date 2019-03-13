# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

'''test tasks
from challenge.tasks import add
res=add.delay(5,5)
res.get()

[2019-03-13 16:23:40,109: INFO/MainProcess] Received task: challenge.tasks.add[7ece318f-4f51-4e8e-8319-7a66f890d173]
[2019-03-13 16:23:40,110: INFO/MainProcess] Task challenge.tasks.add[7ece318f-4f51-4e8e-8319-7a66f890d173] succeeded in 0.0s: 10
'''

@shared_task
def add(x, y):
	return x + y


@shared_task
def mul(x, y):
	return x * y


@shared_task
def xsum(numbers):
	return sum(numbers)
	
#task for check submit (submit_upload), id of Submission
from .models import Submission
import os
from django.conf import settings

@shared_task
def check_submit(id):
	submit = Submission.objects.get(id=id)
	filepath = submit.filepath.path
	file = open(os.path.join(settings.BASE_DIR, filepath))
	linecount = len(file.readlines(  ))
	file.close()
	print(linecount)
	return linecount
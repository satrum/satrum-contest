from django.db import models

# Create your models here.
from django.conf import settings #for User model settings.AUTH_USER_MODEL
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Contest(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=100,verbose_name="title of contest")
	text =  models.TextField(default='', max_length=1000, verbose_name="description of contest")
	org =   models.CharField(max_length=100,verbose_name="name of contest organization")
	creation_time = models.DateTimeField(default=timezone.now)
	reg_deadline  = models.DateTimeField(blank=True, null=True) #blank=True, null=True
	CONTEST_STATUS = (
		('a', 'added'),
		('r', 'registration'),
		('s', 'started'),
		('p', 'paused'),
		('e', 'ended'),
	)
	status = models.CharField(max_length=1, choices=CONTEST_STATUS, blank=True, default='a', help_text='status of Contest')
	
	def __str__(self):
		return self.title
	def get_absolute_url(self):#Returns the url to access a particular contest instance.
		return reverse('contest-detail', args=[str(self.id)])
	def get_lb_url(self):#Returns the url to access a particular contest and leaderboard instance.
		return reverse('contest-lb', args=[str(self.id)])
	def get_sub_url(self):#Returns the url to access a particular contest and authenticated user submissions instance.
		return reverse('contest-submits', args=[str(self.id)])
	def get_upload_url(self):#Returns the url to access a particular contest and form for upload submit.
		return reverse('submit-upload', args=[str(self.id)])

class UserLeaderboard(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_lb")
	contest = models.ForeignKey(Contest, on_delete=models.SET_NULL, null=True, related_name="contest_lb")
	lb_time = models.DateTimeField(default=timezone.now) #update time of lb after submission
	lb_score = models.DecimalField(default=0.0, max_digits=10, decimal_places=6, help_text='last score of user on contest') #update score after submission
	lb_sub_count = models.IntegerField(default=0, help_text='user submissions count') #full count of submission
	lb_sub_count_period = models.IntegerField(default=0, help_text='user submissions count for last period')
	RANK = (
		('g', 'gold'),
		('s', 'silver'),
		('b', 'bronze'),
		('u', 'unranked'),
	)
	lb_rank = models.CharField(max_length=1, choices=RANK, default='u', help_text='rank of user for contest')
	
	class Meta:
		unique_together = ('user', 'contest')

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

def validate_file_size(value):
	filesize = value.size
	if filesize > 10485760:
		raise ValidationError("The maximum file size that can be uploaded is 10MB")
	else:
		return value

import os
def content_file_name(instance, filename):
	ext = filename.split('.')[-1]
	#time = str(timezone.now())
	#print(instance.contest.id, instance.user.id, ext)
	filename = "%s.%s" % (instance.user.id, ext)
	#print(os.path.join('submit_files', filename))
	return os.path.join('submit_files', str(instance.contest.id), filename)

class Submission(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_submission")
	contest = models.ForeignKey(Contest, on_delete=models.SET_NULL, null=True, related_name="contest_submission")
	sub_time = models.DateTimeField(default=timezone.now) #submission time
	sub_text = models.CharField(max_length=200,verbose_name="submission text")
	sub_score = models.DecimalField(default=0.0, max_digits=10, decimal_places=6, help_text='submission score')
	SUB_STATUS = (
		('u', 'uploaded'),
		('c', 'calculated'),
		('e', 'error format'),
		('t', 'time error'), #many submission by period, contest not started
	)
	sub_status = models.CharField(max_length=1, choices=SUB_STATUS, blank=True, default='u', help_text='status of submission')
	#!!! file
	filename = models.CharField(max_length=100, default='') #?
	filepath = models.FileField(upload_to=content_file_name, verbose_name="", 
								validators=[validate_file_size, FileExtensionValidator(allowed_extensions=['csv'])],
								default='')
	#filepath = models.FileField(upload_to='submit_files/', verbose_name="", default='')
	# class Meta:
		# unique_together = ('user', 'contest')

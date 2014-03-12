from django.db import models
from django.contrib.auth.models import User

class PomeloUser(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User)

class Gift(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=20)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	message = models.CharField(max_length=500, null=True)
	url_video = models.CharField(max_length=500, null=True)
	sender = models.ForeignKey(PomeloUser, related_name='sender')
	receiver = models.ForeignKey(PomeloUser, related_name='receiver')
	
	def __unicode__(self):
		return self.name

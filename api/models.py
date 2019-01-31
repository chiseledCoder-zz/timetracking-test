from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_out
# Create your models here.


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='profile')
	last_logout = models.DateTimeField()
	total_hours = models.CharField(null=True, max_length=20)

	def __str__(self):
		return self.user.username

	def represent_total_time(self):
		totsec = int(self.total_hours)
		hours, remainder = divmod(totsec, 3600)
		minutes, seconds = divmod(remainder, 60)
		return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))


def record_logout_timestamp(sender, user, request, **kwargs):
	profile, created = UserProfile.objects.get_or_create(user=user,
														defaults={
															'last_logout': datetime.now()
														})
	custom_format = '%Y-%m-%d %H:%M:%S'
	last_login = datetime.strftime(user.last_login, custom_format)
	current_time = datetime.strftime(datetime.now(), custom_format)
	total_time = datetime.strptime(current_time, custom_format) - datetime.strptime(last_login, custom_format)
	if not created:
		total_time = int(profile.total_hours) + int(total_time.total_seconds())
		profile.total_hours = str(total_time)
		profile.save()


user_logged_out.connect(record_logout_timestamp)

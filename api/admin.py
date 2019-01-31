from django.contrib import admin
from .models import UserProfile
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'represent_total_time']
	ordering = ['-total_hours']


admin.site.register(UserProfile, UserProfileAdmin)

from django.contrib import admin
# from django.contrib.auth.admin import User
from .models import Complain,UserProfile, Profile


# class ComplainTables(admin.ModelAdmin):

admin.site.register(Complain)
admin.site.register(UserProfile)
admin.site.register(Profile)



from django.contrib import admin
# from django.contrib.auth.admin import User
from .models import Complain


# class ComplainTables(admin.ModelAdmin):

admin.site.register(Complain)



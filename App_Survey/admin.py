from django.contrib import admin
# from django.contrib.auth.admin import User
from .models import Complain,UserProfile, Profile, SiteSettings


class ComplainTables(admin.ModelAdmin):
    list_display = ['id','student_name','student_id','feedback_status','submitted_at' ]  
    search_fields = ['student_id']


admin.site.register(Complain,ComplainTables)
admin.site.register(UserProfile)
admin.site.register(Profile)
admin.site.register(SiteSettings)



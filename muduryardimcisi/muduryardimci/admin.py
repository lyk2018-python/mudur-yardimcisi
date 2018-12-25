from django.contrib import admin
from .models import Site,Check,Courses,Profile
admin.site.register(Profile)
admin.site.register(Site)
admin.site.register(Courses)

@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('course_id','user_id',"check_morning",'check_afternoon','check_evening','check_date')
    list_filter = ['course_id__course_name', "check_morning", 'check_afternoon', 'check_evening','check_date']
    search_fields = ['user_id__username','course_id__course_name']
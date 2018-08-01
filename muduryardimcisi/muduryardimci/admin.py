from django.contrib import admin
from .models import Site,Check,Courses,Note,Profile
admin.site.register(Profile)
admin.site.register(Site)
admin.site.register(Courses)
admin.site.register(Note)

@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('course_id','user_id','course_check',"check_morning",'check_afternoon','check_evening')
    list_filter = ['course_id__course_name', 'course_check', "check_morning", 'check_afternoon', 'check_evening']
    search_fields = ['course_check','user_id__username','course_id__course_name']
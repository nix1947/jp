from django.contrib import admin

from .models import Job, Category, Location, Industry, Skill


# Register your models here.

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    search_fields = ['title',]
    list_filter = ['company', 'job_type', 'job_level',  'posted_date', 'deadline',]

    list_display = ('title',  'company', 'status','posted_date', 'deadline', 'created_date',)
    ordering = ['-created_date']


admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Skill)

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    pass

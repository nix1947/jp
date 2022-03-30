from django.contrib import admin

from .models import Job, Category, Location, Industry, Skill




# Register your models here.
admin.site.register(Job)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Skill)
admin.site.register(Industry)


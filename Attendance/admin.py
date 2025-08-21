from django.contrib import admin

from .models import Subject, Period, Attend, ReplacementInfo
# Register your models here.
admin.site.register(Subject)
admin.site.register(Period)
admin.site.register(Attend)
admin.site.register(ReplacementInfo)

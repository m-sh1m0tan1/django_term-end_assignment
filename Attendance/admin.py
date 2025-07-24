from django.contrib import admin
from .models import User, Subject, Period, Attend, ReplacementInfo
# Register your models here.
admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Period)
admin.site.register(Attend)
admin.site.register(ReplacementInfo)

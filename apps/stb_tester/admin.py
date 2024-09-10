from django.contrib import admin
from ..stb_tester.models import StbConfiguration, StbResult
from solo.admin import SingletonModelAdmin
# Register your models here.


admin.site.register(StbConfiguration)
admin.site.register(StbResult)

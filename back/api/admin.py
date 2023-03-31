from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Doctorcomment)
admin.site.register(Correctpic)
admin.site.register(Patientpic)

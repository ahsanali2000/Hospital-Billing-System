from django.contrib import admin
from .models import prescription,patient,doctor,invoice1

admin.site.register(prescription)
admin.site.register(patient)
admin.site.register(doctor)
admin.site.register(invoice1)
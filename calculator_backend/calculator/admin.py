from django.contrib import admin
from .models import Operation, Record, CustomUser

admin.site.register(Operation)
admin.site.register(Record)
admin.site.register(CustomUser)
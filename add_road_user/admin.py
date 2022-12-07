from django.contrib import admin
from .models import User, OffenceList, Crime, Challan,create_roadUser


# Register your models here.
admin.site.register(User)
admin.site.register( OffenceList)
admin.site.register(Crime)
admin.site.register(Challan)
admin.site.register(create_roadUser)

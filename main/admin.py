from django.contrib import admin
from .models import User, Group

class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)

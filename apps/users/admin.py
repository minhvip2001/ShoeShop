from apps.users.models.permission import Permission
from django.contrib import admin
from .models import User
from .models import Role
from .models import Permission

class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Role, UserAdmin)
admin.site.register(Permission, UserAdmin)


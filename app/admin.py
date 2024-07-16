from django.contrib import admin
from app.models import DXVLUsers
from django.contrib.auth.admin import  UserAdmin as OriginalAdmin

class DXVLUsersAdmin(OriginalAdmin):
    list_display = ('username', 'email', 'date_joined',)
    fieldsets = (
        *OriginalAdmin.fieldsets,
        (
            'User Accounts Information',
            {
                'fields': (
                    'user_address',
                    'user_mobile_number',
                )
            }
        )
    )
    list_filter = ('date_joined',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')

admin.site.register(DXVLUsers, DXVLUsersAdmin)
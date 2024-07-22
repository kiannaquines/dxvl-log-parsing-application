from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from app.models import *
from django.contrib.auth.admin import UserAdmin as OriginalAdmin

class DXVLLogsAdmin(admin.ModelAdmin):
    list_display = ('artist', 'date_aired','status','advertisement','added_by', 'date_added')
    search_fields = ('date_aired', 'artist', 'advertisement')
    list_filter = ('date_aired', 'added_by','artist')
    list_per_page = 1000

class DXVLUsersAdmin(OriginalAdmin):
    list_display = ('username', 'email', 'date_joined',)
    fieldsets = (
        (None, {"fields": ("username", "password",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email","user_address","user_mobile_number")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_filter = ('date_joined', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')


class DXVLLogNamesAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_lines', 'file_state')

class DXVLAdvertisementPricesAdmin(admin.ModelAdmin):
    list_display = ('advertisement', 'price')


# admin.site.register(DXVLAdvertisementPrices, DXVLAdvertisementPricesAdmin)
admin.site.register(DXVLLogs, DXVLLogsAdmin)
admin.site.register(DXVLUsers, DXVLUsersAdmin)
admin.site.register(DXVLLogNames, DXVLLogNamesAdmin)
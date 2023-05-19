from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    CustomUser,
    Profile,
    Ad,
    FavoriteAd,
)
# Register your models here.
class MyUserAdmin(BaseUserAdmin):
    list_display = ('email', 'date_joined', 'last_login', 'is_admin', 'is_active',)
    search_fields = ('email',)
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ('email',)
    fieldsets = ()

    add_fieldsets=  (
        (None, {
            'classes':('wide'),
            'fields':('email', 'name', 'surname', 'password1', 'password2')
        }),
    )

    ordering=('email',)

admin.site.register(CustomUser, MyUserAdmin)
admin.site.register(Profile)
admin.site.register(Ad)
admin.site.register(FavoriteAd)
# Register your models here.

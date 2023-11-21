from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import UserCreationForm, UserChangeForm
from .models import User, OtpCode


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('name', 'family', 'email', 'phone_number', 'is_admin')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        ('Main',
         {'fields': ('email', 'name', 'family', 'phone_number', 'password', 'address', 'card_number')}),
        ('permissions', {'fields': ('is_active', 'is_admin',)})
    )

    add_fieldsets = (
        (None, {'fields': (
            'email', 'name', 'family', 'phone_number', 'password1', 'password2', 'address',
            'card_number')})
    ),

    search_fields = ('phone_number', 'name', 'email')
    ordering = ('register_date',)
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)

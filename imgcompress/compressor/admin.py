from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import UserAccounts,Upload
# Register your models here.

@admin.register(UserAccounts)
class UserAccountsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        # (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('id','email', 'first_name', 'last_name', 'is_staff')


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ('id','uploaded_image','current_size','size_after','action','compress_percentage','orignal_size_x_y','resize_measure_x','resize_measure_y','will_be_delete_at')

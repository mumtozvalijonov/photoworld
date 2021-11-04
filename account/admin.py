from django.contrib import admin

from account.models import Account

# Register your models here.


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = ('username', 'email')

    def has_delete_permission(self, request, *args, **kwargs) -> bool:
        return request.user.is_admin and super().has_delete_permission(request, *args, **kwargs)

    def has_add_permission(self, request, *args, **kwargs) -> bool:
        return request.user.is_admin and super().has_delete_permission(request, *args, **kwargs)

    def has_change_permission(self, request, *args, **kwargs) -> bool:
        return request.user.is_admin and super().has_delete_permission(request, *args, **kwargs)

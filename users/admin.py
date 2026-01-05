from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # فیلدهای فقط خواندنی (non-editable)
    readonly_fields = ('date_joined', 'last_login')

    # fieldsets اصلی UserAdmin را گسترش می‌دهیم
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone_number', 'address', 'avatar')
        }),
    )

    # بخش Important dates را دوباره تعریف می‌کنیم تا readonly باشد (اختیاری اما توصیه می‌شود)
    # اگر نخواهید این بخش نمایش داده شود، این قسمت را حذف کنید
    fieldsets = (
        *UserAdmin.fieldsets,  # همه بخش‌های پیش‌فرض
        ('Additional Info', {
            'fields': ('phone_number', 'address', 'avatar')
        }),
    )

    # اگر می‌خواهید date_joined و last_login نمایش داده شوند، یک بخش جدا اضافه کنید
    # یا از روش بالا استفاده کنید و فقط readonly_fields را ست کنید

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'address', 'avatar')
        }),
    )

    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']

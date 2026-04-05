from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserModel


# config tampilan admin
class StaffAdmin(UserAdmin):
    model = UserModel

    # list view
    list_display = ("username", "nama", "role", "is_active", "is_staff")

    # filter sidebar kanan
    list_filter = ("role", "is_active", "is_staff")

    # search bar
    search_fields = ("username", "nama")

    ordering = ("username",)

    # form edit user
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Info Personal", {"fields": ("nama", "role")}),
        ("Hak Akses", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Tanggal", {"fields": ("last_login", "date_joined")}),
    )

    # form tambah user/staff
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "nama", "role", "password1", "password2"),
            },
        ),
    )


# regist ke admin panel
admin.site.register(UserModel, StaffAdmin)

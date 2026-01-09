from django.contrib import admin
from .models import CustomUser, UserHistory

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "role", "is_staff", "is_superuser")
    search_fields = ("email", "full_name")

@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "created_at")
    list_filter = ("action", "created_at")
    search_fields = ("user__email", "user__full_name")

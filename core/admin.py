from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'roll_number', 'house', 'is_active')
    list_filter = ('house', 'is_active')
    search_fields = ('username', 'roll_number')
    ordering = ('username',)

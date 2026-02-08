from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("roll_no", "name", "gender", "house")
    
    search_fields = ("roll_no", "name")
    
    list_filter = ("house", "gender")
    
    ordering = ("roll_no",)

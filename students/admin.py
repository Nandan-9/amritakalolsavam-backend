from django.contrib import messages

from django.contrib import admin
from .models import Student, StudentImport
import pandas as pd
from io import BytesIO

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("roll_no", "name", "gender", "house")
    
    search_fields = ("roll_no", "name")
    
    list_filter = ("house", "gender")
    
    ordering = ("roll_no",)


@admin.register(StudentImport)
class StudentImportAdmin(admin.ModelAdmin):
    list_display = ("id", "uploaded_at")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        try:
            # Read uploaded file directly (no filesystem dependency)
            excel_data = obj.file.read()
            df = pd.read_excel(BytesIO(excel_data))

            created_count = 0
            updated_count = 0

            for _, row in df.iterrows():
                student, created = Student.objects.update_or_create(
                    roll_no=str(row["RollNo"]).strip(),
                    defaults={
                        "name": str(row["Student Name"]).strip(),
                        "gender": str(row["Gender"]).strip(),
                        "house": str(row["House"]).strip(),
                    }
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

            # Delete file after processing (optional but recommended)
            obj.file.delete(save=False)

            self.message_user(
                request,
                f"Import successful. Created: {created_count}, Updated: {updated_count}",
                level=messages.SUCCESS
            )

        except Exception as e:
            self.message_user(
                request,
                f"Import failed: {str(e)}",
                level=messages.ERROR
            )
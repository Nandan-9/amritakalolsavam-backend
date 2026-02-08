import pandas as pd
from django.core.management.base import BaseCommand
from students.models import Student

class Command(BaseCommand):
    help = "Import students from Excel file"

    def handle(self, *args, **kwargs):
        df = pd.read_excel("/home/das/pro/amritakalolsavam-backend/2025ASE-ASC.xlsx")  # path to your file

        for _, row in df.iterrows():
            Student.objects.update_or_create(
                roll_no=str(row["RollNo"]),
                defaults={
                    "name": row["Student Name"],
                    "gender": row["Gender"],
                    "house": row["House"],
                }
            )

        self.stdout.write(self.style.SUCCESS("Students imported successfully"))

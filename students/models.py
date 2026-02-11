from django.db import models

class Student(models.Model):
    roll_no = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    house = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.roll_no} - {self.name}"

class StudentImport(models.Model):
    file = models.FileField(upload_to="temp_imports/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Import {self.id}"

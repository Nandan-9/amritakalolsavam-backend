from ..models import Student



def get_student_meta(roll_number):
    student = Student.objects.filter(roll_no = roll_number).first()
    if not student :
        return None
    return {
        "name" : student.name,
        "house" : student.house.lower()
    }
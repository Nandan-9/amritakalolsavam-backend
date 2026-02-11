from ..models import Student



def get_student_meta(roll_number):
    student = Student.objects.filter(roll_no = roll_number).first()
    if not student :
        return None
    return {
        "name" : student.name,
        "house" : student.house.lower()
    }

def validate_same_house(users):
    houses = {
        user.student.house.lower()
        for user in users
        if hasattr(user, "student") and user.student
    }
    return len(houses) == 1

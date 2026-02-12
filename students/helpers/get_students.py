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
    houses = set()

    for user in users:
        meta = get_student_meta(user.roll_number)

        if not meta:
            return False 

        houses.add(meta["house"].strip().lower())

    return len(houses) == 1


from ..models import User

def get_user_by_id(roll_number):
    try:
        return User.objects.get(roll_number=roll_number)
    except User.DoesNotExist:
        return None

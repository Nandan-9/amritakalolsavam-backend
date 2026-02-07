

from ..models import User

def get_user_by_id(id):
    try:
        return User.objects.get(id=id)
    except User.DoesNotExist:
        return None

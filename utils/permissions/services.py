
# import models
from accounts.models import CustomUser


# create utils hare
def check_staff_permission(*, user: CustomUser, positions: list):
    if user.staff_profile.position.name in positions:
        return True
    return False
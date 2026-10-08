from permission.core.base import BasePermissionWithBypass


# create staff permission hare
class StaffBoundaryPermission(BasePermissionWithBypass):

    def check_object_permission(self, request, view, obj):
        user = request.user

        if user.role == "staff":
            
            # staff self edit permission 
            if user.uuid == obj.uuid:
                print("akhn thekei retun hoyejabe")
                return True
            
            # other permission denied 
            if obj.role in ["admin", "staff"]:
                return False

        return True
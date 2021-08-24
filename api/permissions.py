from rest_framework import permissions

# this class is for give the permissions to owner of obj.
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.username == request.user
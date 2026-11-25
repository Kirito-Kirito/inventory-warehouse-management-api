from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsStaffOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return bool(user.is_staff or user.is_superuser)



class IsAuthenticatedDeleteStaffOnly(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if request.method == 'DELETE':
            return bool(
                user.is_superuser
                or user.is_staff
                or getattr(user, 'role', None) in ('ADMIN', 'MANAGER')
            )

        return True
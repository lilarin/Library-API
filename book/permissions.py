from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission
)


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow only admin users to create, update, or delete books.
    All users (even those not authenticated) can list books.
    """
    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS
            )
            or (request.user and request.user.is_staff)
        )

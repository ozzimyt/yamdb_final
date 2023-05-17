from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Право на изменение имеет только администратор,
    все остальные имеют только возможность чтения.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class IsAuthorOrModeRatOrOrAdminOrReadOnly(permissions.BasePermission):
    """
    Право на изменение имеет только администратор,
    автор или модератор все остальные имеют только
    возможность чтения.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdminUser(permissions.BasePermission):
    """
    Право на изменение имеет только администратор или
    суперюзер
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.is_admin
            )
        )

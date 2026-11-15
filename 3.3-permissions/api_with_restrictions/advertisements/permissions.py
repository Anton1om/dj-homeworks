from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Изменять/удалять объект может только его автор или администратор"""

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        # Администраторы могут всё.
        if request.user and request.user.is_staff:
            return True

        return obj.creator == request.user
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsEditorOrReadOnly(BasePermission):
    message = "Hanya editor yang dapat mengubah experience."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return user.is_authenticated and (
            user.is_superuser or user.groups.filter(name="Editor").exists()
        )

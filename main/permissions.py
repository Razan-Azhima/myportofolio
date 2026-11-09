from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    message = "Hanya pemilik portofolio yang dapat menambah atau menghapus experience."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return (
            request.method in ("PUT", "PATCH")
            and user.groups.filter(name="Editor").exists()
        )

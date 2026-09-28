def editor_flag(request):
    u = request.user
    return {
        "is_editor": u.is_authenticated and (u.is_superuser or u.groups.filter(name="Editor").exists())
    }
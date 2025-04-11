from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedOrReadAdmin(IsAuthenticated):
    """
    Allow read access to authenticated users,
    but limit write operations to admins.
    """

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return False

        # Allow GET for any authenticated user
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Require admin for other methods
        return request.user.is_staff

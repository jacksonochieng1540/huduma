from django.core.exceptions import PermissionDenied
from core.models import User

class StaffRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != User.STAFF:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
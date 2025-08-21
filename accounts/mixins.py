from django.core.exceptions import PermissionDenied

class ForTeachersMixin:
    allowed_roles = [1]
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role not in self.allowed_roles:
            raise PermissionDenied('権限がありません。')
        return super().dispatch(request, *args, **kwargs)
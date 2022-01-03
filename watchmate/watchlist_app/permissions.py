from rest_framework.permissions import IsAdminUser,BasePermission,SAFE_METHODS


class IsAdminOrReadOnly(IsAdminUser):
    def has_permission(self,request,view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)

class IsReviewUserOrReadOnly(BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return obj.review_user == request.user or request.user.is_staff

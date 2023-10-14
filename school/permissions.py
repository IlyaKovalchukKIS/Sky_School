from rest_framework.permissions import BasePermission

from users.models import UserRole


class IsManager(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == UserRole.MANAGER:
            return True
        return False


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsManagerNotCreate(BasePermission):

    def has_permission(self, request, view):
        if request.user.role != UserRole.MANAGER:
            return True
        return False


class IsSuperuser(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False


# class IsOwnerView(BasePermission):
#
#     def has_permission(self, request, view):
#         if request.user == view.get_object().owner:
#             return view.objects.filter(owner=request.user)
#         return False

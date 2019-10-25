from rest_framework.permissions import BasePermission

from FruitGP2.models import FruitUser


class LoginPermission(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user,FruitUser)
    def has_object_permission(self, request, view, obj):
        return obj.user.id==request.user.id
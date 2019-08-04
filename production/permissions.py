from rest_framework import permissions
from django.contrib.auth import authenticate

class UpdateOwnProUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id  

class CreateOwnProduction(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user.id == request.user.id  
    
class UpdateOwnProduction(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user 
    
class ViewOwnProduction(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if obj.user_id == request.user.id:
                return True
            else:
                return False
        else: 
            if obj.user_id == request.user.id:
                return True
            else:
                return False
from rest_framework import permissions
from django.contrib.auth.models import User ## Default Django User Model

# this class is for give the permissions to owner of obj.

class IsOwner(permissions.BasePermission):
      def has_object_permission(self, request, view, obj):
           return obj.User == request.user
           
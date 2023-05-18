from rest_framework.permissions import BasePermission,SAFE_METHODS
from apps.utils.enum import UserType
from apps.todo.models import AddContent,TaskManager


class TaskAddpermission(BasePermission):

    def has_permission(self, request, view):
        if  request.method in SAFE_METHODS:
           return True
        return bool(request.user and request.user.user_type =="admin" or request.user.user_type =="editor")
    

class FeedbackPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type =="admin" or request.user.user_type =="editor")


class AddContentPermission(BasePermission):
    def has_permission(self, request, view):
         if request.method in ['DELETE']:
           return False
         return bool(request.user and request.user.user_type== UserType.content_writer.value)


class ViewContentPermission(BasePermission):
      def has_permission(self, request, view):
         return bool(request.user and request.user.user_type==UserType.editor.value or request.user.user_type==UserType.admin.value)
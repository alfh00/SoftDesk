from rest_framework import permissions
from .models import Project

class IsContributor(permissions.BasePermission):
    message = 'Your must be a part of this ressource to perform this action.'

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True  # Superusers can perform any action


        project_id = view.kwargs.get('project_id') or view.kwargs.get('pk')

        is_contributor = Project.objects.filter(contributors=request.user, uuid=project_id).exists()
        

        return is_contributor

class IsAuthor(permissions.BasePermission):
    message = 'You are not the owner of this ressource to perform this action.'

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True  # Superusers can perform any action

        if request.method in permissions.SAFE_METHODS:
            return True  # Safe methods (GET, HEAD, OPTIONS) are allowed

        project_id =  view.kwargs.get('project_id') or view.kwargs.get('pk')

        is_author = Project.objects.filter(author=request.user, uuid=project_id).exists()
        
        return is_author
    
class IsAuthorA(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is the author of the object (project, issue, or comment)
        return obj.author == request.user

